"""
validator.py
Valide un fichier XML ou JSON
Retourne un objet structuré : valide ou pas, erreur matchée, ligne/colonne, ET correction auto si possible
"""

import json
import xml.etree.ElementTree as ET
import re
import os
from errors_matcher import match_error
from corrector import auto_correct, can_auto_correct


# ==============================
# ✨ NOUVEAU : CHARGEMENT SCHÉMAS
# ==============================
def load_schema(file_type, version="1.28"):
    """
    Charge un schéma de validation JSON pour un type de fichier DayZ.
    
    Args:
        file_type (str): Type de fichier ('types', 'events', 'economy')
        version (str): Version DayZ (par défaut '1.28')
    
    Returns:
        dict: Schéma de validation JSON ou None si erreur
    """
    # Chemin relatif depuis la racine du projet
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_path, f"schemas/dayz_{version}/{file_type}.json")
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Schéma non trouvé : {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de lecture du schéma : {e}")
        return None


# ==============================
# ✨ NOUVEAU : DÉTECTION TYPE FICHIER
# ==============================
def detect_dayz_file_type(content):
    """
    Détecte automatiquement le type de fichier DayZ (types, events, economy, globals, messages).
    
    Args:
        content (str): Contenu XML du fichier
    
    Returns:
        str: Type détecté ('types', 'events', 'economy', 'globals', 'messages') ou None
    """
    try:
        root = ET.fromstring(content)
        root_tag = root.tag
        
        # Détection par balise racine
        if root_tag == "types":
            return "types"
        elif root_tag == "events":
            return "events"
        elif root_tag == "economy":
            return "economy"
        elif root_tag == "variables":
            return "globals"
        elif root_tag == "messages":
            return "messages"
        
        return None
    except:
        return None


# ==============================
# ✨ NOUVEAU : VALIDATION SÉMANTIQUE
# ==============================
def validate_semantic_rules(content, file_type):
    """
    Valide un fichier XML selon les règles métier DayZ (validation sémantique).
    
    Args:
        content (str): Contenu XML du fichier
        file_type (str): Type de fichier ('types', 'events', 'economy', 'globals')
    
    Returns:
        list: Liste de warnings/erreurs sémantiques
            [{"severity": "error"|"warning", "message": "...", "line": int}]
    """
    schema = load_schema(file_type)
    if not schema:
        return []
    
    warnings = []
    
    try:
        tree = ET.fromstring(content)
        
        # VALIDATION TYPES.XML
        if file_type == "types":
            warnings.extend(_validate_types_semantic(tree, schema))
        
        # VALIDATION EVENTS.XML
        elif file_type == "events":
            warnings.extend(_validate_events_semantic(tree, schema))
        
        # VALIDATION ECONOMY.XML
        elif file_type == "economy":
            warnings.extend(_validate_economy_semantic(tree, schema))
        
    except ET.ParseError:
        # Si parsing échoue, pas de validation sémantique (déjà géré par validate_xml)
        pass
    
    return warnings


# ==============================
# ✨ VALIDATION SÉMANTIQUE : TYPES.XML
# ==============================
def _validate_types_semantic(root, schema):
    """Valide les règles métier de types.xml"""
    warnings = []
    
    for idx, type_elem in enumerate(root.findall('type'), start=1):
        item_name = type_elem.get('name', f'Item #{idx}')
        
        # Récupérer les valeurs
        nominal = int(type_elem.findtext('nominal', '0'))
        min_val = int(type_elem.findtext('min', '0'))
        quantmin = int(type_elem.findtext('quantmin', '-1'))
        quantmax = int(type_elem.findtext('quantmax', '-1'))
        lifetime = int(type_elem.findtext('lifetime', '0'))
        
        # RÈGLE 1: min ≤ nominal
        if min_val > nominal:
            warnings.append({
                "severity": "error",
                "message": f"Item '{item_name}': min ({min_val}) > nominal ({nominal}). Le minimum ne peut pas être supérieur au nominal.",
                "line": idx
            })
        
        # RÈGLE 2: quantmin ≤ quantmax
        if quantmin != -1 and quantmax != -1 and quantmin > quantmax:
            warnings.append({
                "severity": "error",
                "message": f"Item '{item_name}': quantmin ({quantmin}) > quantmax ({quantmax}). La quantité minimum ne peut pas être supérieure au maximum.",
                "line": idx
            })
        
        # RÈGLE 3: lifetime > 0
        if lifetime <= 0:
            warnings.append({
                "severity": "error",
                "message": f"Item '{item_name}': lifetime ({lifetime}) doit être > 0.",
                "line": idx
            })
        
        # RÈGLE 4: Item désactivé mais min > 0
        if nominal == 0 and min_val > 0:
            warnings.append({
                "severity": "warning",
                "message": f"Item '{item_name}': nominal=0 (désactivé) mais min={min_val}. Recommandation : mettre min=0.",
                "line": idx
            })
        
        # RÈGLE 5: Pas de <usage> = pas de spawn
        usages = type_elem.findall('usage')
        if nominal > 0 and len(usages) == 0:
            flags = type_elem.find('flags')
            crafted = flags.get('crafted', '0') if flags is not None else '0'
            if crafted == '0':
                warnings.append({
                    "severity": "warning",
                    "message": f"Item '{item_name}': nominal={nominal} mais aucun <usage> défini. Cet item ne spawnera pas naturellement.",
                    "line": idx
                })
    
    return warnings


# ==============================
# ✨ VALIDATION SÉMANTIQUE : EVENTS.XML
# ==============================
def _validate_events_semantic(root, schema):
    """Valide les règles métier de events.xml"""
    warnings = []
    
    for idx, event_elem in enumerate(root.findall('event'), start=1):
        event_name = event_elem.get('name', f'Event #{idx}')
        
        # Récupérer les valeurs
        nominal = int(event_elem.findtext('nominal', '0'))
        min_val = int(event_elem.findtext('min', '0'))
        max_val = int(event_elem.findtext('max', '0'))
        lifetime = int(event_elem.findtext('lifetime', '0'))
        active = int(event_elem.findtext('active', '1'))
        
        # RÈGLE 1: min ≤ nominal ≤ max
        if not (min_val <= nominal <= max_val):
            warnings.append({
                "severity": "error",
                "message": f"Event '{event_name}': La relation min ({min_val}) ≤ nominal ({nominal}) ≤ max ({max_val}) n'est pas respectée.",
                "line": idx
            })
        
        # RÈGLE 2: lifetime > 0
        if lifetime <= 0:
            warnings.append({
                "severity": "error",
                "message": f"Event '{event_name}': lifetime ({lifetime}) doit être > 0.",
                "line": idx
            })
        
        # RÈGLE 3: Event désactivé
        if active == 0:
            warnings.append({
                "severity": "warning",
                "message": f"Event '{event_name}': active=0 (désactivé). Est-ce voulu ?",
                "line": idx
            })
        
        # RÈGLE 4: Children min/max
        for child in event_elem.findall('.//child'):
            child_type = child.get('type', 'unknown')
            child_min = int(child.get('min', '0'))
            child_max = int(child.get('max', '0'))
            lootmin = int(child.get('lootmin', '0'))
            lootmax = int(child.get('lootmax', '0'))
            
            if child_min > child_max:
                warnings.append({
                    "severity": "error",
                    "message": f"Event '{event_name}', child '{child_type}': min ({child_min}) > max ({child_max}).",
                    "line": idx
                })
            
            if lootmin > lootmax:
                warnings.append({
                    "severity": "error",
                    "message": f"Event '{event_name}', child '{child_type}': lootmin ({lootmin}) > lootmax ({lootmax}).",
                    "line": idx
                })
    
    return warnings


# ==============================
# ✨ VALIDATION SÉMANTIQUE : ECONOMY.XML
# ==============================
def _validate_economy_semantic(root, schema):
    """Valide les règles métier de economy.xml"""
    warnings = []
    
    # Vérifier building respawn=0
    building = root.find('building')
    if building is not None:
        respawn = building.get('respawn', '0')
        if respawn != '0':
            warnings.append({
                "severity": "error",
                "message": f"Système 'building': respawn doit être 0 (les bases ne doivent PAS respawner). Actuellement : {respawn}",
                "line": 0
            })
    
    # Vérifier player = 1 1 1 1
    player = root.find('player')
    if player is not None:
        init = player.get('init', '0')
        load = player.get('load', '0')
        respawn = player.get('respawn', '0')
        save = player.get('save', '0')
        
        if not (init == '1' and load == '1' and respawn == '1' and save == '1'):
            warnings.append({
                "severity": "warning",
                "message": f"Système 'player': configuration inhabituelle détectée. Vanilla recommandé : init='1' load='1' respawn='1' save='1'. Actuel : init='{init}' load='{load}' respawn='{respawn}' save='{save}'",
                "line": 0
            })
    
    # Vérifier systèmes critiques (dynamic, vehicles, building)
    for system_name in ['dynamic', 'vehicles', 'building']:
        system = root.find(system_name)
        if system is not None:
            save = system.get('save', '0')
            load = system.get('load', '0')
            
            if save == '0' or load == '0':
                warnings.append({
                    "severity": "warning",
                    "message": f"Système CRITIQUE '{system_name}': save={save} ou load={load} détecté. ATTENTION : perte de données au restart !",
                    "line": 0
                })
            
            # Incohérence load=1 sans save=1
            if load == '1' and save == '0':
                warnings.append({
                    "severity": "warning",
                    "message": f"Système '{system_name}': load=1 mais save=0. Rien ne sera sauvegardé, donc rien à charger. Est-ce voulu ?",
                    "line": 0
                })
    
    return warnings


# ==============================
# RÉSULTAT — Structure de retour
# ==============================
# Tout passe par ce dictionnaire. app.py ne lit que ça.
#
# {
#     "valid": bool,
#     "file_type": "xml" ou "json",
#     "dayz_type": str ou None,          → ✨ NOUVEAU : type DayZ détecté
#     "error": {
#         "line": int,
#         "column": int,
#         "message_brut": str,
#         "matched": dict ou None,
#     },
#     "formatted": str ou None,
#     "corrected": str ou None,
#     "semantic_warnings": list ou None   → ✨ NOUVEAU : warnings sémantiques
# }


# ==============================
# VALIDATION JSON
# ==============================
def validate_json(content):
    """Valide du contenu JSON. Retourne le dict de résultat."""
    result = {
        "valid": False,
        "file_type": "json",
        "dayz_type": None,
        "error": None,
        "formatted": None,
        "corrected": None,
        "semantic_warnings": None
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
        
        # Tenter la correction automatique si possible
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
        "dayz_type": None,
        "error": None,
        "formatted": None,
        "corrected": None,
        "semantic_warnings": None
    }

    try:
        root = ET.fromstring(content)
        
        # ✨ NOUVEAU : Détection type DayZ
        dayz_type = detect_dayz_file_type(content)
        result["dayz_type"] = dayz_type
        
        # Valide → on formate avec indentation
        result["valid"] = True
        result["formatted"] = _format_xml(content)
        
        # ✨ NOUVEAU : Validation sémantique si type DayZ détecté
        if dayz_type in ['types', 'events', 'economy']:
            semantic_warnings = validate_semantic_rules(content, dayz_type)
            if semantic_warnings:
                result["semantic_warnings"] = semantic_warnings
        
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
        
        # Tenter la correction automatique si possible
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
        "dayz_type": None,
        "error": {
            "line": 0,
            "column": 0,
            "message_brut": "Type de fichier non supporté",
            "matched": None
        },
        "formatted": None,
        "corrected": None,
        "semantic_warnings": None
    }
