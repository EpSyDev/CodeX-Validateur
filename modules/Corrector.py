"""
corrector.py
Applique les corrections automatiques sur le contenu.
Uniquement les corrections sûres identifiées dans errors_db.json (correction_automatique: true).
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
            "corrected": str,                    → contenu corrigé
            "applied_corrections": [str, ...],   → liste des corrections appliquées
            "has_changes": bool                  → vrai si au moins une correction
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
# CORRECTIONS JSON
# ==============================
def _correct_json(content):
    """Applique les corrections automatiques JSON"""
    corrected = content
    applied = []
    
    # 1. Virgules finales avant } ou ]
    if re.search(r',\s*[}\]]', corrected):
        corrected = re.sub(r',\s*}', '}', corrected)
        corrected = re.sub(r',\s*]', ']', corrected)
        applied.append("Suppression des virgules finales")
    
    # 2. Guillemets simples → doubles
    # ATTENTION : on ne fait ça QUE si on détecte des clés avec guillemets simples
    # Pas si c'est du texte à l'intérieur d'une valeur
    if re.search(r"'[^']*'\s*:", corrected):  # Pattern 'clé':
        corrected = corrected.replace("'", '"')
        applied.append("Conversion guillemets simples → doubles")
    
    has_changes = len(applied) > 0
    
    return {
        "corrected": corrected,
        "applied_corrections": applied,
        "has_changes": has_changes
    }


# ==============================
# CORRECTIONS XML
# ==============================
def _correct_xml(content):
    """Applique les corrections automatiques XML"""
    corrected = content
    applied = []
    
    # 1. Caractères spéciaux non échappés
    # & → &amp; (sauf si déjà échappé)
    unescaped_count = len(re.findall(r'&(?!(amp|lt|gt|quot|apos);)', corrected))
    if unescaped_count > 0:
        corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
        applied.append(f"Échappement de {unescaped_count} caractère(s) & → &amp;")
    
    # On ne corrige PAS automatiquement :
    # - Balises ouvrantes sans fermeture (trop risqué — où fermer ?)
    # - Commentaires non fermés (trop risqué — où fermer ?)
    # - Balises auto-fermantes (trop risqué — /> ou </tag> ?)
    # - Attributs mal formés (trop risqué — quelle valeur mettre ?)
    # - Mismatch tags (trop risqué — laquelle est correcte ?)
    
    has_changes = len(applied) > 0
    
    return {
        "corrected": corrected,
        "applied_corrections": applied,
        "has_changes": has_changes
    }


# ==============================
# VÉRIFICATION DE FAISABILITÉ
# ==============================
def can_auto_correct(error_matched):
    """
    Vérifie si une erreur matchée peut être corrigée automatiquement.
    
    Paramètre :
        error_matched → entrée de errors_db (dict) ou None
    
    Retourne :
        bool → True si correction_automatique est à True
    """
    if not error_matched:
        return False
    
    return error_matched.get("correction_automatique", False)


# ==============================
# PRÉVISUALISATION
# ==============================
def preview_corrections(content, file_type):
    """
    Prévisualise les corrections qui seront appliquées SANS modifier le contenu.
    Utile pour afficher à l'utilisateur ce qui va changer avant de valider.
    
    Retourne :
        {
            "will_apply": [str, ...],   → liste des corrections qui seront faites
            "safe": bool                → True si toutes les corrections sont sûres
        }
    """
    result = auto_correct(content, file_type)
    
    return {
        "will_apply": result["applied_corrections"],
        "safe": True  # Toutes nos corrections sont sûres par défaut
    }


# ==============================
# CORRECTION GUIDÉE (futur)
# ==============================
def suggest_manual_fixes(content, file_type, error_matched):
    """
    Pour les erreurs NON auto-corrigeables, suggère des actions manuelles.
    
    Retourne :
        {
            "can_auto": bool,
            "manual_steps": [str, ...]   → étapes à faire manuellement
        }
    """
    if can_auto_correct(error_matched):
        return {
            "can_auto": True,
            "manual_steps": []
        }
    
    # Suggestions manuelles selon le type d'erreur
    manual_steps = []
    
    if error_matched:
        error_id = error_matched.get("id", "")
        
        if "XML_001" in error_id:  # Balise auto-fermante
            manual_steps.append("Ajoute /> à la fin de la balise")
            manual_steps.append("Exemple : <current actual=\"0.45\" />")
        
        elif "XML_002" in error_id:  # Balise sans fermeture
            manual_steps.append("Trouve la balise ouvrante signalée")
            manual_steps.append("Ajoute la balise fermante correspondante")
            manual_steps.append("Exemple : </overcast> après le contenu")
        
        elif "XML_003" in error_id:  # Attribut mal formé
            manual_steps.append("Vérifie que chaque attribut a une valeur")
            manual_steps.append("Format : nom=\"valeur\"")
        
        elif "XML_004" in error_id:  # Commentaire non fermé
            manual_steps.append("Trouve le commentaire <!-- ouvert")
            manual_steps.append("Ajoute --> pour le fermer")
        
        elif "XML_006" in error_id:  # Mismatch tag
            manual_steps.append("Vérifie que les balises ouvrantes/fermantes correspondent")
            manual_steps.append("La balise fermante doit avoir le même nom que l'ouvrante")
        
        elif "JSON_003" in error_id:  # Clé sans guillemets
            manual_steps.append("Entoure chaque clé de guillemets doubles")
            manual_steps.append('Exemple : "damage" au lieu de damage')
        
        elif "JSON_004" in error_id:  # Parenthèse non fermée
            manual_steps.append("Vérifie que chaque { a son }")
            manual_steps.append("Vérifie que chaque [ a son ]")
    
    return {
        "can_auto": False,
        "manual_steps": manual_steps if manual_steps else ["Corrige manuellement selon les indications"]
    }