"""
errors_matcher.py
Matche une erreur détectée par le validateur avec errors_db.json
Retourne le bon message, les exemples, et le niveau (novice/modder)
✨ AMÉLIORÉ : Extrait le nom exact des balises problématiques
"""

import json
import re
from pathlib import Path

# ==============================
# CHARGEMENT DE LA BASE
# ==============================
def load_errors_db():
    """Charge errors_db.json depuis le dossier data/"""
    db_path = Path(__file__).parent.parent / "data" / "errors_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)["errors"]

# Cache en mémoire pour ne pas relire le fichier à chaque fois
_ERRORS_DB = None

def get_errors_db():
    global _ERRORS_DB
    if _ERRORS_DB is None:
        _ERRORS_DB = load_errors_db()
    return _ERRORS_DB


# ==============================
# ✨ NOUVEAU : EXTRACTION NOM BALISE
# ==============================
def extract_tag_name_from_error(error_msg, content, line_num):
    """
    Extrait le nom de la balise problématique depuis le message d'erreur ou le contenu.
    
    Args:
        error_msg: Message d'erreur du parseur
        content: Contenu complet du fichier
        line_num: Numéro de ligne de l'erreur
    
    Returns:
        str: Nom de la balise ou None
    """
    # Essayer d'extraire depuis le message d'erreur
    # Ex: "mismatched tag: line 3, column 2" ou "Opening and ending tag mismatch: territory"
    tag_match = re.search(r'tag[:\s]+(\w+)', error_msg, re.IGNORECASE)
    if tag_match:
        return tag_match.group(1)
    
    # Si pas dans le message, chercher dans la ligne problématique
    lines = content.split('\n')
    if 0 < line_num <= len(lines):
        problem_line = lines[line_num - 1]
        
        # Chercher balise fermante
        closing_tag = re.search(r'</(\w+)>', problem_line)
        if closing_tag:
            return closing_tag.group(1)
        
        # Chercher balise ouvrante
        opening_tag = re.search(r'<(\w+)', problem_line)
        if opening_tag:
            return opening_tag.group(1)
    
    return None


def find_unclosed_tag_name(content, error_line):
    """
    Trouve le nom de la balise qui n'est pas fermée.
    
    Args:
        content: Contenu XML complet
        error_line: Ligne où l'erreur est détectée
    
    Returns:
        str: Nom de la balise non fermée ou None
    """
    lines = content.split('\n')
    open_tags = []
    
    # Parser jusqu'à la ligne d'erreur
    for i, line in enumerate(lines[:error_line], start=1):
        # Ignorer commentaires
        line_clean = re.sub(r'<!--.*?-->', '', line)
        
        # Ignorer balises auto-fermantes
        line_clean = re.sub(r'<[^>]+/>', '', line_clean)
        
        # Trouver balises fermantes
        closing_tags = re.findall(r'</(\w+)>', line_clean)
        for tag in closing_tags:
            if open_tags and open_tags[-1] == tag:
                open_tags.pop()
        
        # Trouver balises ouvrantes
        opening_tags = re.findall(r'<(\w+)(?:\s[^>]*)?>(?![^<]*/>)', line_clean)
        for tag in opening_tags:
            open_tags.append(tag)
    
    # La dernière balise ouverte = balise non fermée
    return open_tags[-1] if open_tags else None


# ==============================
# MATCHING — JSON
# ==============================
def match_json_error(content, error):
    """
    Prend le contenu du fichier + l'erreur JSONDecodeError
    Retourne l'entrée correspondante de errors_db ou None
    """
    db = get_errors_db()
    msg = str(error).lower()

    # Virgule finale avant } ou ]
    if re.search(r',\s*[}\]]', content):
        return _get_by_id("JSON_001")

    # Guillemets simples
    if "'" in content and ("expecting" in msg or "expecting property" in msg):
        return _get_by_id("JSON_002")

    # Clé sans guillemets
    if "expecting property name" in msg:
        return _get_by_id("JSON_003")

    # Accolade / crochet non fermé
    if _check_parentheses_balance(content):
        return _get_by_id("JSON_004")

    return None


# ==============================
# MATCHING — XML
# ==============================
def match_xml_error(content, error):
    """
    Prend le contenu du fichier + l'erreur ParseError
    Retourne l'entrée correspondante de errors_db ou None
    ✨ AMÉLIORÉ : Ajoute le nom de la balise dans le résultat
    """
    msg = str(error).lower()
    error_line = error.position[0] if hasattr(error, 'position') else 0

    # Commentaire non fermé (vérifie en premier — bloque tout le reste)
    if _check_unclosed_comment(content):
        return _get_by_id("XML_004")

    # Caractère spécial non échappé
    if re.search(r'&(?!(amp|lt|gt|quot|apos);)', content):
        return _get_by_id("XML_005")

    # ✨ Mismatch tag (balise fermante qui ne correspond pas)
    if "mismatched tag" in msg or "opening and ending tag mismatch" in msg:
        matched = _get_by_id("XML_006")
        if matched:
            tag_name = extract_tag_name_from_error(str(error), content, error_line)
            if tag_name:
                # Enrichir les messages avec le nom exact
                matched = matched.copy()
                matched["message_novice"] = matched["message_novice"].replace(
                    "comme </fog>", 
                    f"</{tag_name}>"
                )
                matched["message_modder"] = matched["message_modder"] + f" Balise problématique : <{tag_name}>"
                matched["tag_name"] = tag_name
        return matched

    # ✨ Balise ouvrante sans fermeture
    if "no element found" in msg or "unclosed token" in msg:
        matched = _get_by_id("XML_002")
        if matched:
            tag_name = find_unclosed_tag_name(content, error_line)
            if tag_name:
                # Enrichir les messages avec le nom exact
                matched = matched.copy()
                matched["message_novice"] = matched["message_novice"].replace(
                    "<overcast>",
                    f"<{tag_name}>"
                ).replace(
                    "</overcast>",
                    f"</{tag_name}>"
                )
                matched["message_modder"] = matched["message_modder"] + f" Balise non fermée : <{tag_name}>"
                matched["tag_name"] = tag_name
        return matched

    # Attribut mal formé
    if "not well-formed" in msg or "syntax error" in msg:
        # Vérifie si c'est vraiment un attribut
        if _check_malformed_attribute(content):
            return _get_by_id("XML_003")
        # Sinon c'est probablement une balise auto-fermante mal écrite
        if _check_missing_self_close(content):
            return _get_by_id("XML_001")

    return None


# ==============================
# CHECKS INTERNES
# ==============================
def _check_parentheses_balance(content):
    """Vérifie si les { } [ ] sont bien équilibrés"""
    return (
        content.count("{") != content.count("}") or
        content.count("[") != content.count("]")
    )

def _check_unclosed_comment(content):
    """Vérifie s'il y a un commentaire XML non fermé"""
    opens = [m.start() for m in re.finditer(r'<!--', content)]
    closes = [m.start() for m in re.finditer(r'-->', content)]
    return len(opens) > len(closes)

def _check_malformed_attribute(content):
    """Vérifie s'il y a un attribut mal formé dans le contenu"""
    # Attribut sans valeur : name= sans guillemets après
    if re.search(r'\w+=\s*[^"\s>]', content):
        return True
    # Attribut avec = mais rien après
    if re.search(r'\w+=\s*[>\/]', content):
        return True
    return False

def _check_missing_self_close(content):
    """Vérifie les balises qui devraient être auto-fermantes mais ne le sont pas"""
    # Liste des balises connues comme auto-fermantes dans DayZ
    self_closing_tags = [
        "current", "limits", "timelimits", "changelimits",
        "thresholds", "storm", "item", "type", "zone"
    ]
    for tag in self_closing_tags:
        # Cherche une balise ouverte sans /> ni </tag>
        pattern = rf'<{tag}\s[^>]*[^/]>'
        if re.search(pattern, content):
            return True
    return False


# ==============================
# RÉCUPÉRATION PAR ID
# ==============================
def _get_by_id(error_id):
    """Retourne l'entrée de errors_db correspondant à l'id"""
    db = get_errors_db()
    for entry in db:
        if entry["id"] == error_id:
            return entry
    return None


# ==============================
# FONCTION PRINCIPALE
# ==============================
def match_error(content, error, file_type):
    """
    Fonction principale appelée par validator.py
    
    Paramètres :
        content   → contenu brut du fichier
        error     → exception levée (JSONDecodeError ou ParseError)
        file_type → "json" ou "xml"
    
    Retourne :
        dict avec : id, titre, message_novice, message_modder,
                    exemple_avant, exemple_après, correction_automatique
                    ✨ + tag_name si balise détectée
        ou None si rien ne matche
    """
    if file_type == "json":
        return match_json_error(content, error)
    elif file_type == "xml":
        return match_xml_error(content, error)
    return None
