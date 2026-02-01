"""
comparator.py
Génère un diff lisible entre le code avant et après correction.
Affichage côte à côte pour que l'utilisateur voie exactement ce qui a changé.
"""

import re
from difflib import unified_diff


# ==============================
# FONCTION PRINCIPALE
# ==============================
def compare_before_after(before, after):
    """
    Compare deux versions d'un fichier et génère un diff lisible.
    
    Paramètres :
        before → contenu original (string)
        after  → contenu corrigé (string)
    
    Retourne :
        {
            "has_changes": bool,
            "changes_count": int,
            "diff_text": str,           → diff formaté pour affichage
            "summary": str              → résumé en une ligne
        }
    """
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    
    # Si identiques
    if before == after:
        return {
            "has_changes": False,
            "changes_count": 0,
            "diff_text": "",
            "summary": "Aucune modification détectée."
        }
    
    # Génère le diff
    diff = list(unified_diff(
        before_lines,
        after_lines,
        lineterm='',
        n=1  # 1 ligne de contexte autour de chaque changement
    ))
    
    # Compte les changements réels (ignore les lignes de métadonnées)
    changes_count = sum(1 for line in diff if line.startswith('+') or line.startswith('-'))
    changes_count = changes_count - 2  # On retire les lignes --- et +++
    
    # Formate pour affichage
    diff_text = _format_diff(diff, before_lines, after_lines)
    
    # Résumé
    summary = f"{changes_count} modification(s) appliquée(s)."
    
    return {
        "has_changes": True,
        "changes_count": changes_count,
        "diff_text": diff_text,
        "summary": summary
    }


# ==============================
# FORMATAGE DU DIFF
# ==============================
def _format_diff(diff, before_lines, after_lines):
    """
    Formate le diff pour un affichage clair dans Streamlit.
    Retourne un texte avec marqueurs visuels.
    """
    formatted = []
    
    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            # Ignore les métadonnées
            continue
        
        elif line.startswith('@@'):
            # Ligne de contexte (numéros de lignes)
            formatted.append(f"\n{line}\n")
        
        elif line.startswith('-'):
            # Ligne supprimée (code avant)
            formatted.append(f"❌ AVANT  : {line[1:]}")
        
        elif line.startswith('+'):
            # Ligne ajoutée (code après)
            formatted.append(f"✅ APRÈS  : {line[1:]}")
        
        else:
            # Ligne de contexte (inchangée)
            formatted.append(f"   {line}")
    
    return "\n".join(formatted)


# ==============================
# COMPARAISON CÔTE À CÔTE (alternative)
# ==============================
def compare_side_by_side(before, after):
    """
    Génère une comparaison côte à côte ligne par ligne.
    Plus simple que unified_diff, mieux pour Streamlit avec colonnes.
    
    Retourne :
        {
            "before_lines": [(num, content, is_changed), ...],
            "after_lines": [(num, content, is_changed), ...],
            "changes_count": int
        }
    """
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    
    max_len = max(len(before_lines), len(after_lines))
    
    before_formatted = []
    after_formatted = []
    changes_count = 0
    
    for i in range(max_len):
        before_line = before_lines[i] if i < len(before_lines) else ""
        after_line = after_lines[i] if i < len(after_lines) else ""
        
        is_changed = before_line != after_line
        if is_changed:
            changes_count += 1
        
        before_formatted.append((i + 1, before_line, is_changed))
        after_formatted.append((i + 1, after_line, is_changed))
    
    return {
        "before_lines": before_formatted,
        "after_lines": after_formatted,
        "changes_count": changes_count
    }


# ==============================
# RÉSUMÉ DES CHANGEMENTS
# ==============================
def get_changes_summary(before, after):
    """
    Analyse les changements et retourne un résumé détaillé.
    
    Retourne :
        {
            "lines_added": int,
            "lines_removed": int,
            "lines_modified": int,
            "specific_changes": [str, ...]   → liste des changements identifiés
        }
    """
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    
    # Diff basique
    diff = list(unified_diff(before_lines, after_lines, lineterm=''))
    
    lines_added = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    lines_removed = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    
    # Lignes modifiées = on compare ligne par ligne
    lines_modified = 0
    for i in range(min(len(before_lines), len(after_lines))):
        if before_lines[i] != after_lines[i]:
            lines_modified += 1
    
    # Changements spécifiques identifiés
    specific_changes = _identify_specific_changes(before, after)
    
    return {
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "lines_modified": lines_modified,
        "specific_changes": specific_changes
    }


# ==============================
# IDENTIFICATION DES CHANGEMENTS SPÉCIFIQUES
# ==============================
def _identify_specific_changes(before, after):
    """
    Identifie des changements spécifiques connus (virgules, guillemets, etc.)
    """
    changes = []
    
    # Virgules finales supprimées
    before_trailing_commas = len(re.findall(r',\s*[}\]]', before))
    after_trailing_commas = len(re.findall(r',\s*[}\]]', after))
    if before_trailing_commas > after_trailing_commas:
        removed = before_trailing_commas - after_trailing_commas
        changes.append(f"Suppression de {removed} virgule(s) finale(s)")
    
    # Guillemets simples → doubles
    before_single_quotes = before.count("'")
    after_single_quotes = after.count("'")
    if before_single_quotes > after_single_quotes:
        changes.append("Conversion guillemets simples → doubles")
    
    # Caractères spéciaux échappés
    before_unescaped = len(re.findall(r'&(?!(amp|lt|gt|quot|apos);)', before))
    after_unescaped = len(re.findall(r'&(?!(amp|lt|gt|quot|apos);)', after))
    if before_unescaped > after_unescaped:
        escaped = before_unescaped - after_unescaped
        changes.append(f"Échappement de {escaped} caractère(s) spéciaux (&)")
    
    # Balises auto-fermantes ajoutées
    before_self_close = before.count('/>')
    after_self_close = after.count('/>')
    if after_self_close > before_self_close:
        added = after_self_close - before_self_close
        changes.append(f"Ajout de {added} fermeture(s) auto-fermante(s) (/>)")
    
    # Indentation corrigée
    before_indent_avg = _avg_indent(before)
    after_indent_avg = _avg_indent(after)
    if abs(after_indent_avg - before_indent_avg) > 0.5:
        changes.append("Correction de l'indentation")
    
    return changes if changes else ["Modifications mineures"]


# ==============================
# UTILITAIRES
# ==============================
def _avg_indent(content):
    """Calcule l'indentation moyenne (en espaces) du contenu"""
    lines = [line for line in content.splitlines() if line.strip()]
    if not lines:
        return 0
    
    total_indent = 0
    for line in lines:
        spaces = len(line) - len(line.lstrip(' '))
        total_indent += spaces
    
    return total_indent / len(lines)