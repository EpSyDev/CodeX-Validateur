"""
corrector.py - VERSION AMÉLIORÉE
Applique les corrections automatiques sur le contenu XML et JSON
Corrections basiques et sûres uniquement
"""

import re
import json
from pathlib import Path


# ==============================
# CHARGEMENT DE LA BASE
# ==============================
def load_errors_db():
    """Charge errors_db.json pour savoir quelles corrections sont auto"""
    db_path = Path(__file__).parent.parent / "data" / "errors_db.json"
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)["errors"]

_ERRORS_DB = None

def get_errors_db():
    global _ERRORS_DB
    if _ERRORS_DB is None:
        _ERRORS_DB = load_errors_db()
    return _ERRORS_DB


# ==============================
# CORRECTIONS XML
# ==============================

def fix_xml_self_closing_tags(content):
    """
    Corrige les balises auto-fermantes mal écrites
    <current actual="0.45"> → <current actual="0.45" />
    """
    corrected = content
    applied = []
    
    # Liste des balises DayZ connues comme auto-fermantes
    self_closing_tags = [
        'current', 'fog', 'overcast', 'rain', 'storm',
        'hoarder', 'damage', 'usage', 'value', 'category',
        'tier', 'cargo', 'item'
    ]
    
    for tag in self_closing_tags:
        # Pattern : <tag ...> (sans /> et sans contenu ni </tag>)
        pattern = rf'<{tag}(\s[^>]*)?(?<!/)>'
        
        # Vérifier qu'il n'y a pas de </tag> après
        matches = list(re.finditer(pattern, corrected))
        
        for match in reversed(matches):  # Parcourir à l'envers pour ne pas décaler les positions
            tag_content = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            
            # Vérifier qu'il n'y a pas de balise fermante correspondante
            after_tag = corrected[end_pos:end_pos+100]
            if f'</{tag}>' not in after_tag:
                # C'est bien une balise qui devrait être auto-fermante
                corrected_tag = tag_content[:-1] + ' />'
                corrected = corrected[:start_pos] + corrected_tag + corrected[end_pos:]
                applied.append(f"Ajout de /> à la balise <{tag}>")
    
    return corrected, applied


def fix_xml_unclosed_comments(content):
    """
    Corrige les commentaires XML non fermés
    <!-- commentaire → <!-- commentaire -->
    """
    corrected = content
    applied = []
    
    # Compter les <!-- et les -->
    open_count = content.count('<!--')
    close_count = content.count('-->')
    
    if open_count > close_count:
        # Il manque des fermetures
        missing = open_count - close_count
        corrected += '\n' + ('-->\n' * missing)
        applied.append(f"Fermeture de {missing} commentaire(s) XML")
    
    return corrected, applied


def fix_xml_unescaped_chars(content):
    """
    Échappe les caractères spéciaux XML
    & → &amp; (sauf si déjà échappé)
    """
    corrected = content
    applied = []
    
    # Échapper & qui ne sont pas déjà échappés
    unescaped_count = len(re.findall(r'&(?!(amp|lt|gt|quot|apos);)', corrected))
    if unescaped_count > 0:
        corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
        applied.append(f"Échappement de {unescaped_count} caractère(s) &")
    
    return corrected, applied


def fix_xml_unclosed_tags(content):
    """
    Détecte et ferme les balises XML non fermées
    """
    lines = content.split('\n')
    open_tags = []
    applied = []
    
    for line_num, line in enumerate(lines, start=1):
        # Ignorer commentaires
        line_clean = re.sub(r'<!--.*?-->', '', line)
        
        # Ignorer balises auto-fermantes
        line_clean = re.sub(r'<[^>]+/>', '', line_clean)
        
        # Trouver balises fermantes
        closing_tags = re.findall(r'</(\w+)>', line_clean)
        for tag in closing_tags:
            if open_tags and open_tags[-1][0] == tag:
                open_tags.pop()
        
        # Trouver balises ouvrantes
        opening_tags = re.findall(r'<(\w+)(?:\s[^>]*)?>(?![^<]*/>)', line_clean)
        for tag in opening_tags:
            open_tags.append((tag, line_num, line))
    
    # Ajouter les balises fermantes manquantes
    if open_tags:
        corrected = content
        for tag_name, line_num, original_line in reversed(open_tags):
            indent = len(original_line) - len(original_line.lstrip())
            closing_tag = '\n' + (' ' * indent) + f'</{tag_name}>'
            corrected += closing_tag
            applied.append(f"Ajout de </{tag_name}>")
        
        return corrected, applied
    
    return content, []


def _correct_xml(content):
    """Applique toutes les corrections automatiques XML"""
    corrected = content
    all_applied = []
    
    # 1. Balises auto-fermantes
    corrected, applied = fix_xml_self_closing_tags(corrected)
    all_applied.extend(applied)
    
    # 2. Caractères non échappés
    corrected, applied = fix_xml_unescaped_chars(corrected)
    all_applied.extend(applied)
    
    # 3. Commentaires non fermés
    corrected, applied = fix_xml_unclosed_comments(corrected)
    all_applied.extend(applied)
    
    # 4. Balises non fermées
    corrected, applied = fix_xml_unclosed_tags(corrected)
    all_applied.extend(applied)
    
    return {
        "corrected": corrected,
        "applied_corrections": all_applied,
        "has_changes": len(all_applied) > 0
    }


# ==============================
# CORRECTIONS JSON
# ==============================

def fix_json_trailing_commas(content):
    """
    Supprime les virgules finales avant } ou ]
    {"key": "value",} → {"key": "value"}
    """
    corrected = content
    applied = []
    
    if re.search(r',\s*[}\]]', corrected):
        corrected = re.sub(r',\s*}', '}', corrected)
        corrected = re.sub(r',\s*]', ']', corrected)
        applied.append("Suppression des virgules finales")
    
    return corrected, applied


def fix_json_single_quotes(content):
    """
    Convertit les guillemets simples en doubles
    {'key': 'value'} → {"key": "value"}
    """
    corrected = content
    applied = []
    
    # Remplacer ' par " SEULEMENT pour les clés (pattern 'clé':)
    if re.search(r"'[^']*'\s*:", corrected):
        corrected = corrected.replace("'", '"')
        applied.append("Conversion guillemets simples → doubles")
    
    return corrected, applied


def fix_json_missing_quotes(content):
    """
    Ajoute des guillemets aux clés sans guillemets
    {key: "value"} → {"key": "value"}
    """
    corrected = content
    applied = []
    
    # Pattern pour détecter clés sans guillemets
    pattern = r'(\{|,)\s*([a-zA-Z_]\w*)\s*:'
    matches = list(re.finditer(pattern, corrected))
    
    if matches:
        # Parcourir à l'envers pour ne pas décaler les positions
        for match in reversed(matches):
            key_name = match.group(2)
            full_match = match.group(0)
            
            # Remplacer par version avec guillemets
            prefix = match.group(1)
            replacement = f'{prefix} "{key_name}":'
            
            start = match.start()
            end = match.end()
            corrected = corrected[:start] + replacement + corrected[end:]
        
        applied.append(f"Ajout de guillemets à {len(matches)} clé(s)")
    
    return corrected, applied


def fix_json_unclosed_brackets(content):
    """
    Ferme les accolades/crochets manquants
    {"key": "value" → {"key": "value"}
    """
    corrected = content
    applied = []
    
    # Compter les accolades et crochets
    open_braces = content.count('{')
    close_braces = content.count('}')
    open_brackets = content.count('[')
    close_brackets = content.count(']')
    
    # Ajouter les fermetures manquantes
    if open_braces > close_braces:
        missing = open_braces - close_braces
        corrected += '\n' + ('}' * missing)
        applied.append(f"Fermeture de {missing} accolade(s)")
    
    if open_brackets > close_brackets:
        missing = open_brackets - close_brackets
        corrected += '\n' + (']' * missing)
        applied.append(f"Fermeture de {missing} crochet(s)")
    
    return corrected, applied


def _correct_json(content):
    """Applique toutes les corrections automatiques JSON"""
    corrected = content
    all_applied = []
    
    # 1. Virgules finales
    corrected, applied = fix_json_trailing_commas(corrected)
    all_applied.extend(applied)
    
    # 2. Guillemets simples → doubles
    corrected, applied = fix_json_single_quotes(corrected)
    all_applied.extend(applied)
    
    # 3. Clés sans guillemets
    corrected, applied = fix_json_missing_quotes(corrected)
    all_applied.extend(applied)
    
    # 4. Accolades/crochets non fermés
    corrected, applied = fix_json_unclosed_brackets(corrected)
    all_applied.extend(applied)
    
    return {
        "corrected": corrected,
        "applied_corrections": all_applied,
        "has_changes": len(all_applied) > 0
    }


# ==============================
# FONCTION PRINCIPALE
# ==============================
def auto_correct(content, file_type):
    """
    Applique les corrections automatiques au contenu.
    
    Paramètres :
        content   → contenu brut du fichier
        file_type → "json" ou "xml"
    
    Retourne :
        {
            "corrected": str,
            "applied_corrections": [str, ...],
            "has_changes": bool
        }
    """
    if file_type == "json":
        return _correct_json(content)
    elif file_type == "xml":
        return _correct_xml(content)
    
    # Type inconnu → aucune correction
    return {
        "corrected": content,
        "applied_corrections": [],
        "has_changes": False
    }


# ==============================
# VÉRIFICATION DE FAISABILITÉ
# ==============================
def can_auto_correct(error_matched):
    """
    Vérifie si une erreur matchée peut être corrigée automatiquement.
    
    Retourne :
        bool → True si correction possible
    """
    if not error_matched:
        return False
    
    # Liste étendue des erreurs auto-corrigeables
    auto_correctable_ids = [
        "XML_001",  # Balise auto-fermante
        "XML_002",  # Balise non fermée
        "XML_004",  # Commentaire non fermé
        "XML_005",  # Caractères non échappés
        "XML_006",  # Balises mismatch
        "JSON_001", # Virgule finale
        "JSON_002", # Guillemets simples
        "JSON_003", # Clé sans guillemets
        "JSON_004"  # Accolade non fermée
    ]
    
    if error_matched.get("id") in auto_correctable_ids:
        return True
    
    return error_matched.get("correction_automatique", False)


# ==============================
# PRÉVISUALISATION
# ==============================
def preview_corrections(content, file_type):
    """
    Prévisualise les corrections qui seront appliquées.
    
    Retourne :
        {
            "will_apply": [str, ...],
            "safe": bool
        }
    """
    result = auto_correct(content, file_type)
    
    return {
        "will_apply": result["applied_corrections"],
        "safe": True
    }


# ==============================
# SUGGESTIONS MANUELLES
# ==============================
def suggest_manual_fixes(content, file_type, error_matched):
    """
    Pour les erreurs NON auto-corrigeables, suggère des actions manuelles.
    
    Retourne :
        {
            "can_auto": bool,
            "manual_steps": [str, ...]
        }
    """
    if can_auto_correct(error_matched):
        return {
            "can_auto": True,
            "manual_steps": []
        }
    
    # Suggestions manuelles
    manual_steps = []
    
    if error_matched:
        error_id = error_matched.get("id", "")
        
        if "XML_003" in error_id:  # Attribut mal formé
            manual_steps.append("Vérifie que chaque attribut a une valeur")
            manual_steps.append("Format : nom=\"valeur\"")
        
        elif "XML_007" in error_id:  # Balise inconnue
            manual_steps.append("Vérifie le nom de la balise")
            manual_steps.append("Consulte la documentation DayZ")
    
    return {
        "can_auto": False,
        "manual_steps": manual_steps if manual_steps else ["Corrige manuellement selon les indications"]
    }
