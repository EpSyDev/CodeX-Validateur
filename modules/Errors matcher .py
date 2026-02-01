"""
errors_matcher.py
Matche une erreur détectée par le validateur avec errors_db.json
Retourne le bon message, les exemples, et le niveau (novice/modder)
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
    """
    msg = str(error).lower()

    # Commentaire non fermé (vérifie en premier — bloque tout le reste)
    if _check_unclosed_comment(content):
        return _get_by_id("XML_004")

    # Caractère spécial non échappé
    if re.search(r'&(?!(amp|lt|gt|quot|apos);)', content):
        return _get_by_id("XML_005")

    # Mismatch tag (balise fermante qui ne correspond pas)
    if "mismatched tag" in msg:
        return _get_by_id("XML_006")

    # Balise ouvrante sans fermeture
    if "no element found" in msg or "unclosed token" in msg:
        return _get_by_id("XML_002")

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
        "thresholds", "storm", "item", "type"
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
        ou None si rien ne matche
    """
    if file_type == "json":
        return match_json_error(content, error)
    elif file_type == "xml":
        return match_xml_error(content, error)
    return None