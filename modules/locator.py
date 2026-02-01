"""
locator.py
Remonte depuis la ligne signalée par le parseur pour trouver la vraie source de l'erreur XML.
Le parseur XML Python remonte souvent l'erreur en fin de fichier alors que la cause réelle est plus haut.
Ce module cherche cette cause réelle.

Utilisé uniquement pour du XML. En JSON, le parseur donne déjà la bonne ligne.
"""

import re


# ==============================
# FONCTION PRINCIPALE
# ==============================
def locate_real_error(content, reported_line):
    """
    Fonction principale appelée par app.py après une erreur XML.
    
    Paramètres :
        content        → contenu brut du fichier XML
        reported_line  → ligne signalée par le parseur (peut être fausse)
    
    Retourne :
        {
            "real_line": int,           → ligne probable de la vraie cause
            "confidence": str,          → "haute" / "moyenne" / "faible"
            "reason": str,              → explication en français pourquoi cette ligne
            "reported_line": int        → ligne du parseur (pour comparaison)
        }
    """
    lines = content.splitlines()

    # Si le fichier est vide ou la ligne invalide
    if not lines or reported_line < 1:
        return _no_result(reported_line)

    # On cherche dans cet ordre de priorité
    checks = [
        _find_unclosed_comment,
        _find_unclosed_tag,
        _find_orphan_closing_tag,
        _find_malformed_attribute,
        _find_unescaped_special_char,
    ]

    for check in checks:
        result = check(lines, reported_line)
        if result:
            return result

    # Rien trouvé → on garde la ligne du parseur
    return _no_result(reported_line)


# ==============================
# CHECK 1 : Commentaire non fermé
# ==============================
def _find_unclosed_comment(lines, reported_line):
    """
    Cherche un <!-- sans --> correspondant.
    Remonte depuis le début du fichier (un commentaire non fermé bloque tout).
    """
    open_count = 0

    for i, line in enumerate(lines):
        opens = len(re.findall(r'<!--', line))
        closes = len(re.findall(r'-->', line))
        open_count += opens - closes

        # Dès qu'on a plus d'ouvertures que de fermetures, c'est ici
        if open_count > 0:
            return {
                "real_line": i + 1,
                "confidence": "haute",
                "reason": f"Commentaire ouvert à la ligne {i + 1} mais jamais fermé avec -->. Tout ce qui suit est ignoré.",
                "reported_line": reported_line
            }

    return None


# ==============================
# CHECK 2 : Balise ouvrante sans fermeture
# ==============================
def _find_unclosed_tag(lines, reported_line):
    """
    Garde une pile des balises ouvrantes.
    Si une balise reste dans la pile à la fin → elle n'a jamais été fermée.
    Remonte depuis le début pour être précis.
    """
    stack = []  # Liste de (nom_balise, numéro_ligne)

    for i, line in enumerate(lines):
        # Ignore les commentaires
        clean_line = re.sub(r'<!--.*?-->', '', line)

        # Balises auto-fermantes → on les ignore
        # <current actual="0.45" />
        auto_close = re.findall(r'<(\w+)[^>]*/>', clean_line)

        # Balises ouvrantes : <overcast> ou <weather reset="0">
        opens = re.findall(r'<(\w+)(?:\s[^>]*)?>',  clean_line)

        # Balises fermantes : </overcast>
        closes = re.findall(r'</(\w+)>', clean_line)

        # Ajoute les ouvrantes (sauf auto-fermantes et déclaration XML)
        # On skip aussi les balises avec un attribut mal formé → laissées pour _find_malformed_attribute
        for tag in opens:
            if tag not in auto_close and tag != '?xml':
                if not re.search(r'\w+=\s*[>\/]', line) and not re.search(r'\w+=\s*[^"\s>][^>]*>', line):
                    stack.append((tag, i + 1))

        # Retire les fermantes de la pile
        for tag in closes:
            found = False
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == tag:
                    stack.pop(j)
                    found = True
                    break
            # Si la fermante ne correspond à rien dans la pile → c'est un mismatch
            # On laisse _find_orphan_closing_tag gérer ce cas (message plus précis)
            if not found:
                return None

    # Si la pile n'est pas vide → balise(s) non fermée(s)
    if stack:
        # On prend la première balise non fermée (la plus haute dans le fichier)
        tag_name, line_num = stack[0]
        return {
            "real_line": line_num,
            "confidence": "haute",
            "reason": f"La balise <{tag_name}> ouverte à la ligne {line_num} n'est jamais fermée avec </{tag_name}>.",
            "reported_line": reported_line
        }

    return None


# ==============================
# CHECK 3 : Balise fermante orpheline (mismatch)
# ==============================
def _find_orphan_closing_tag(lines, reported_line):
    """
    Cherche une balise fermante qui ne correspond à aucune ouvrante.
    Exemple : </fog> alors que la balise ouverte était <overcast>
    """
    stack = []

    for i, line in enumerate(lines):
        clean_line = re.sub(r'<!--.*?-->', '', line)

        auto_close = re.findall(r'<(\w+)[^>]*/>', clean_line)
        opens = re.findall(r'<(\w+)(?:\s[^>]*)?>',  clean_line)
        closes = re.findall(r'</(\w+)>', clean_line)

        for tag in opens:
            if tag not in auto_close and tag != '?xml':
                stack.append((tag, i + 1))

        for tag in closes:
            # Cherche dans la pile
            found = False
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == tag:
                    stack.pop(j)
                    found = True
                    break

            # Pas trouvé dans la pile → orpheline
            if not found:
                expected = stack[-1][0] if stack else "inconnue"
                return {
                    "real_line": i + 1,
                    "confidence": "haute",
                    "reason": f"Balise </{tag}> à la ligne {i + 1} ne correspond à rien. La dernière balise ouverte est <{expected}>.",
                    "reported_line": reported_line
                }

    return None


# ==============================
# CHECK 4 : Attribut mal formé
# ==============================
def _find_malformed_attribute(lines, reported_line):
    """
    Cherche un attribut incomplet dans les balises.
    Exemples : max=> ou min= sans valeur
    """
    for i, line in enumerate(lines):
        # Attribut avec = mais pas de valeur entre guillemets après
        if re.search(r'\w+=\s*[>\/]', line):
            return {
                "real_line": i + 1,
                "confidence": "haute",
                "reason": f"Attribut incomplet à la ligne {i + 1}. Format attendu : nom=\"valeur\".",
                "reported_line": reported_line
            }
        # Attribut avec = et une valeur sans guillemets
        if re.search(r'\w+=\s*[^"\s>][^>]*>', line):
            # Vérifie que c'est bien dans une balise XML
            if re.search(r'<\w+', line):
                return {
                    "real_line": i + 1,
                    "confidence": "moyenne",
                    "reason": f"Attribut sans guillemets à la ligne {i + 1}. Entoure la valeur de doubles guillemets.",
                    "reported_line": reported_line
                }

    return None


# ==============================
# CHECK 5 : Caractère spécial non échappé
# ==============================
def _find_unescaped_special_char(lines, reported_line):
    """
    Cherche un & qui n'est pas suivi d'une entité connue (amp; lt; gt; quot; apos;)
    """
    for i, line in enumerate(lines):
        # Ignore les commentaires
        clean_line = re.sub(r'<!--.*?-->', '', line)

        match = re.search(r'&(?!(amp|lt|gt|quot|apos);)', clean_line)
        if match:
            return {
                "real_line": i + 1,
                "confidence": "haute",
                "reason": f"Caractère & non échappé à la ligne {i + 1}. Remplace par &amp;.",
                "reported_line": reported_line
            }

    return None


# ==============================
# RETOUR PAR DÉFAUT
# ==============================
def _no_result(reported_line):
    """Retourne quand on ne trouve rien de mieux que la ligne du parseur"""
    return {
        "real_line": reported_line,
        "confidence": "faible",
        "reason": "Impossible de localiser la cause exacte. Vérifie autour de la ligne indiquée.",
        "reported_line": reported_line
    }