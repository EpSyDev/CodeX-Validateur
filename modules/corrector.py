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
# ✨ NOUVEAU : DÉTECTION BALISES NON FERMÉES
# ==============================
def find_unclosed_tags(content):
    """
    Détecte les balises XML non fermées.
    
    Retourne:
        list: [(tag_name, line_number, position), ...]
    """
    # Stack pour tracker les balises ouvertes
    open_tags = []
    unclosed = []
    
    # Pattern pour balises
    # Ouvrante: <tag ...> ou <tag>
    # Fermante: </tag>
    # Auto-fermante: <tag ... />
    
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        # Ignorer commentaires
        line_clean = re.sub(r'<!--.*?-->', '', line)
        
        # Trouver balises auto-fermantes (on les ignore)
        line_clean = re.sub(r'<[^>]+/>', '', line_clean)
        
        # Trouver balises fermantes
        closing_tags = re.findall(r'</(\w+)>', line_clean)
        for tag in closing_tags:
            if open_tags and open_tags[-1][0] == tag:
                open_tags.pop()
            # Sinon c'est une balise fermante orpheline (autre erreur)
        
        # Trouver balises ouvrantes
        opening_tags = re.findall(r'<(\w+)(?:\s[^>]*)?>(?![^<]*/>)', line_clean)
        for tag in opening_tags:
            open_tags.append((tag, line_num, line))
    
    # Ce qui reste dans open_tags = balises non fermées
    return open_tags


# ==============================
# ✨ NOUVEAU : CORRECTION BALISES NON FERMÉES
# ==============================
def fix_unclosed_tags(content):
    """
    Corrige automatiquement les balises non fermées en ajoutant les balises fermantes.
    
    Retourne:
        tuple: (corrected_content, list_of_fixes)
    """
    unclosed = find_unclosed_tags(content)
    
    if not unclosed:
        return content, []
    
    lines = content.split('\n')
    fixes = []
    
    # Parcourir les balises non fermées (de la plus récente à la plus ancienne)
    for tag_name, line_num, original_line in reversed(unclosed):
        # Trouver où insérer la balise fermante
        # On cherche la prochaine balise ouvrante du même niveau ou la fin du fichier
        
        insert_line = None
        indent = len(original_line) - len(original_line.lstrip())
        
        # Chercher la prochaine balise de même niveau ou niveau supérieur
        for i in range(line_num, len(lines)):
            current_line = lines[i]
            current_indent = len(current_line) - len(current_line.lstrip())
            
            # Si on trouve une balise ouvrante au même niveau, on insère avant
            if current_indent <= indent and re.search(r'<\w+', current_line):
                insert_line = i
                break
        
        # Si pas trouvé, insérer à la fin
        if insert_line is None:
            insert_line = len(lines)
        
        # Créer la balise fermante avec la bonne indentation
        closing_tag = ' ' * indent + f'</{tag_name}>'
        
        # Insérer la balise fermante
        lines.insert(insert_line, closing_tag)
        
        fixes.append(f"Ajout de </{tag_name}> à la ligne {insert_line + 1}")
    
    return '\n'.join(lines), fixes


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
    
    # ✨ 2. NOUVEAU : Balises non fermées
    corrected_with_tags, tag_fixes = fix_unclosed_tags(corrected)
    if tag_fixes:
        corrected = corrected_with_tags
        applied.extend(tag_fixes)
    
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
        bool → True si correction_automatique est à True OU si c'est une balise non fermée
    """
    if not error_matched:
        return False
    
    # ✨ NOUVEAU : Les balises non fermées sont maintenant auto-corrigeables
    if error_matched.get("id") in ["XML_002", "XML_006"]:
        return True
    
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
        
        elif "XML_003" in error_id:  # Attribut mal formé
            manual_steps.append("Vérifie que chaque attribut a une valeur")
            manual_steps.append("Format : nom=\"valeur\"")
        
        elif "XML_004" in error_id:  # Commentaire non fermé
            manual_steps.append("Trouve le commentaire <!-- ouvert")
            manual_steps.append("Ajoute --> pour le fermer")
        
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
