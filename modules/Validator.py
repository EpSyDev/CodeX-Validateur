"""
validator.py
Valide un fichier XML ou JSON
Retourne un objet structuré : valide ou pas, erreur matchée, ligne/colonne
"""

import json
import xml.etree.ElementTree as ET
import re
from errors_matcher import match_error


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
#         "message_brut": str,          → message du parseur (en anglais)
#         "matched": dict ou None,      → entrée de errors_db si matchée
#     },
#     "formatted": str ou None          → code formaté si valide
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
        "formatted": None
    }

    try:
        data = json.loads(content)
        # Valide → on formate proprement
        result["valid"] = True
        result["formatted"] = json.dumps(data, indent=2, ensure_ascii=False)
        return result

    except json.JSONDecodeError as e:
        result["error"] = {
            "line": e.lineno,
            "column": e.colno,
            "message_brut": e.msg,
            "matched": match_error(content, e, "json")
        }
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
        "formatted": None
    }

    try:
        root = ET.fromstring(content)
        # Valide → on formate avec indentation
        result["valid"] = True
        result["formatted"] = _format_xml(content)
        return result

    except ET.ParseError as e:
        line, col = e.position
        result["error"] = {
            "line": line,
            "column": col,
            "message_brut": str(e),
            "matched": match_error(content, e, "xml")
        }
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
        "formatted": None
    }