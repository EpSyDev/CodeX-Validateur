"""
validator.py
Valide un fichier XML ou JSON
Retourne un objet structuré : valide ou pas, erreur matchée, ligne/colonne, ET correction auto si possible
"""

import json
import xml.etree.ElementTree as ET
import re
from errors_matcher import match_error
from corrector import auto_correct, can_auto_correct


# ==============================
# RÉSULTAT — Structure de retour
# ==============================
# Tout passe par ce dictionnaire. app.py ne lit que ça.
#
# {
#     "valid": bool,
#     "file_type": "xml" ou "json",
#     "error": {
#         "line": int,
#         "column": int,
#         "message_brut": str,
#         "matched": dict ou None,
#     },
#     "formatted": str ou None,
#     "corrected": str ou None          → NOUVEAU : contenu corrigé si auto-corrigeable
# }


# ==============================
# VALIDATION JSON
# ==============================
def validate_json(content):
    """Valide du contenu JSON. Retourne le dict de résultat."""
    result = {
        "valid": False,
        "file_type": "json",
        "error": None,
        "formatted": None,
        "corrected": None
    }

    try:
        data = json.loads(content)
        # Valide → on formate proprement
        result["valid"] = True
        result["formatted"] = json.dumps(data, indent=2, ensure_ascii=False)
        return result

    except json.JSONDecodeError as e:
        matched = match_error(content, e, "json")
        
        result["error"] = {
            "line": e.lineno,
            "column": e.colno,
            "message_brut": e.msg,
            "matched": matched
        }
        
        # NOUVEAU : Tenter la correction automatique si possible
        if matched and can_auto_correct(matched):
            correction = auto_correct(content, "json")
            if correction["has_changes"]:
                result["corrected"] = correction["corrected"]
        
        return result


# ==============================
# VALIDATION XML
# ==============================
def validate_xml(content):
    """Valide du contenu XML. Retourne le dict de résultat."""
    result = {
        "valid": False,
        "file_type": "xml",
        "error": None,
        "formatted": None,
        "corrected": None
    }

    try:
        root = ET.fromstring(content)
        # Valide → on formate avec indentation
        result["valid"] = True
        result["formatted"] = _format_xml(content)
        return result

    except ET.ParseError as e:
        line, col = e.position
        matched = match_error(content, e, "xml")
        
        result["error"] = {
            "line": line,
            "column": col,
            "message_brut": str(e),
            "matched": matched
        }
        
        # NOUVEAU : Tenter la correction automatique si possible
        if matched and can_auto_correct(matched):
            correction = auto_correct(content, "xml")
            if correction["has_changes"]:
                result["corrected"] = correction["corrected"]
        
        return result


# ==============================
# FORMATAGE XML
# ==============================
def _format_xml(content):
    """Formate du XML avec indentation propre"""
    try:
        from xml.dom import minidom
        pretty = minidom.parseString(content).toprettyxml(indent="    ")
        # Supprime les lignes vides et la déclaration XML en double
        lines = [line for line in pretty.split("\n") if line.strip()]
        return "\n".join(lines)
    except:
        # Si le formatage échoue, on retourne tel quel
        return content


# ==============================
# FONCTION PRINCIPALE
# ==============================
def validate(content, file_type):
    """
    Fonction principale appelée par app.py
    
    Paramètres :
        content   → contenu brut du fichier (string)
        file_type → "json" ou "xml"
    
    Retourne :
        dict structuré (voir commentaire en haut du fichier)
    """
    if file_type == "json":
        return validate_json(content)
    elif file_type == "xml":
        return validate_xml(content)
    
    # Type inconnu
    return {
        "valid": False,
        "file_type": file_type,
        "error": {
            "line": 0,
            "column": 0,
            "message_brut": "Type de fichier non supporté",
            "matched": None
        },
        "formatted": None,
        "corrected": None
    }
