"""
Codex Suite - Carte Interactive
Éditeur visuel multi-événements : Zombies + Events (véhicules, crashes, gaz...)

🎯 V2 : Ajout parser cfgeventspawns.xml + sélecteur type d'événement
"""

import streamlit as st
import xml.etree.ElementTree as ET
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
from collections import defaultdict

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex - Carte Interactive",
    page_icon="assets/images/favicon.png",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #000000; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px 80px 30px;
}

.page-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 40px;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

.stats-box {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    color: white;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    margin: 6px 0;
}
.stats-box h2 { color: #00D4FF; margin: 0; font-size: 2em; }
.stats-box p  { margin: 4px 0 0 0; font-size: 0.85em; color: rgba(255,255,255,0.6); }

.zone-card {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-left: 4px solid #00D4FF;
    color: rgba(255,255,255,0.85);
    padding: 15px 20px;
    border-radius: 16px;
    margin: 10px 0;
}
.zone-card h4 { color: #00D4FF; margin: 0 0 8px 0; font-size: 16px; font-weight: 700; }
.zone-card p  { margin: 4px 0; font-size: 0.9em; }

.calibration-note {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-left: 4px solid #00D4FF;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 8px;
    color: rgba(255,255,255,0.8);
    font-size: 0.9em;
}

.tip-box {
    background: rgba(0, 25, 50, 0.55);
    border-left: 3px solid #fbbf24;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.85em;
    color: rgba(255,255,255,0.8);
    margin: 8px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
    border: none;
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 5px 18px rgba(0, 212, 255, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
}

/* Tabs Streamlit */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0, 15, 30, 0.8);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(0, 212, 255, 0.2);
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.6);
    font-weight: 600;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 212, 255, 0.15) !important;
    color: #00D4FF !important;
}

/* Radio buttons */
.stRadio > div { gap: 12px; }
.stRadio label {
    background: rgba(0, 25, 50, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    padding: 8px 16px;
    color: rgba(255,255,255,0.8) !important;
    transition: all 0.2s;
}
.stRadio label:has(input:checked) {
    background: rgba(0, 212, 255, 0.15);
    border-color: #00D4FF;
    color: #00D4FF !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# CONFIG CARTES
# ==============================
MAP_CONFIG = {
    'chernarus': {
        'label':   '🗺️ Chernarus ✅',
        'size':    15360,
        'image':   'chernarus_map.jpg',
        'offsets': {'x': 0, 'z': 0},
        'files': {
            'zombies':  'zombie_territories_chernarus.xml',
            'events':   'cfgeventspawns_chernarus.xml',
            'spawns':   'cfgplayerspawnpoints_chernarus.xml',
        }
    },
    'livonia': {
        'label':   '🗺️ Livonia ✅',
        'size':    12800,
        'image':   'livonia_map.jpg',
        'offsets': {'x': 0, 'z': 0},
        'files': {
            'zombies':  'zombie_territories_livonia.xml',
            'events':   'cfgeventspawns_livonia.xml',
            'spawns':   'cfgplayerspawnpoints_livonia.xml',
        }
    },
    'sakhal': {
        'label':   '🗺️ Sakhal ✅',
        'size':    15360,
        'image':   'sakhal_map.webp',
        'offsets': {'x': 0, 'z': -21},
        'files': {
            'zombies':  'zombie_territories_sakhal.xml',
            'events':   'cfgeventspawns_sakhal.xml',
            'spawns':   'cfgplayerspawnpoints_sakhal.xml',
        }
    },
}

# ==============================
# CATÉGORIES D'EVENTS
# ==============================
EVENT_CATEGORIES = {
    '🧟 Zombies':           ['Infected'],
    '🚁 Crashes':           ['StaticHeli', 'StaticSanta', 'StaticAirplane'],
    '☢️ Zones contaminées': ['StaticContaminated'],
    '🚗 Véhicules':         ['Vehicle'],
    '🎖️ Militaire':         ['StaticMilitaryConvoy', 'StaticPoliceCar', 'StaticPoliceSituation'],
    '🐺 Animaux':           ['Animal'],
    '🔥 Divers':            ['StaticBonfire', 'StaticChristmas', 'StaticTrain', 'Item'],
}

def get_event_category(event_name):
    for cat, prefixes in EVENT_CATEGORIES.items():
        for prefix in prefixes:
            if event_name.startswith(prefix):
                return cat
    return '❓ Autre'

# ==============================
# COULEURS
# ==============================
ZOMBIE_COLORS = {
    'InfectedArmy':        '#8B0000',
    'InfectedArmyHard':    '#DC143C',
    'InfectedCity':        '#4169E1',
    'InfectedIndustrial':  '#FF8C00',
    'InfectedVillage':     '#32CD32',
    'InfectedPolice':      '#191970',
    'InfectedMedic':       '#FF1493',
    'InfectedPrisoner':    '#8B4513',
    'InfectedFirefighter': '#FF4500',
    'InfectedReligious':   '#9370DB',
}

EVENT_COLORS = {
    '🚁 Crashes':           '#FFD700',
    '☢️ Zones contaminées': '#39FF14',
    '🚗 Véhicules':         '#00BFFF',
    '🎖️ Militaire':         '#8B8B00',
    '🐺 Animaux':           '#DEB887',
    '🔥 Divers':            '#FF6347',
    '❓ Autre':             '#808080',
}

SPAWN_COLORS = {
    'fresh':  '#00FF7F',
    'hop':    '#FFA500',
    'travel': '#6699CC',
}

def get_point_color(name, source='zombies'):
    if source == 'zombies':
        for key, color in ZOMBIE_COLORS.items():
            if key in name:
                return color
        return '#808080'
    elif source == 'spawns':
        spawn_type = name.split('|')[0] if '|' in name else 'fresh'
        return SPAWN_COLORS.get(spawn_type, '#808080')
    else:
        cat = get_event_category(name)
        return EVENT_COLORS.get(cat, '#808080')

# ==============================
# PARSERS
# ==============================

def parse_zombie_territories(xml_content):
    """Parse zombie_territories.xml"""
    root = ET.fromstring(xml_content)
    zones = []
    for territory in root.findall('territory'):
        color = territory.get('color', '')
        for zone in territory.findall('zone'):
            zones.append({
                'source':    'zombies',
                'name':      zone.get('name'),
                'x':         float(zone.get('x')),
                'z':         float(zone.get('z')),
                'r':         float(zone.get('r')),
                'smin':      int(zone.get('smin')),
                'smax':      int(zone.get('smax')),
                'dmin':      int(zone.get('dmin')),
                'dmax':      int(zone.get('dmax')),
                'smin_orig': int(zone.get('smin')),
                'smax_orig': int(zone.get('smax')),
                'dmin_orig': int(zone.get('dmin')),
                'dmax_orig': int(zone.get('dmax')),
                'color':     color,
                'active':    True,
            })
    return zones


def parse_event_spawns(xml_content):
    """
    Parse cfgeventspawns.xml.
    Conserve TOUS les attributs bruts des <pos> pour export fidèle.
    Conserve la balise <zone> optionnelle si présente.
    """
    root = ET.fromstring(xml_content)
    events = []

    for event in root.findall('event'):
        event_name = event.get('name')
        if not event_name:
            continue

        # Balise <zone> optionnelle
        zone_el = event.find('zone')
        zone_params = dict(zone_el.attrib) if zone_el is not None else None

        # Positions
        positions = list(event.findall('pos'))

        for i, pos in enumerate(positions):
            pos_data = dict(pos.attrib)
            try:
                x = float(pos_data.get('x', 0))
                z = float(pos_data.get('z', 0))
            except ValueError:
                continue

            events.append({
                'source':      'events',
                'name':        event_name,
                'category':    get_event_category(event_name),
                'x':           x,
                'z':           z,
                'pos_attrs':   pos_data,       # brut, conservé pour export
                'zone_params': zone_params,    # brut, conservé pour export
                'pos_index':   i,
                'active':      True,
                # Paramètres spawn (lecture seule depuis zone_params)
                'smin': int(zone_params.get('smin', 0)) if zone_params else 0,
                'smax': int(zone_params.get('smax', 0)) if zone_params else 0,
                'dmin': int(zone_params.get('dmin', 0)) if zone_params else 0,
                'dmax': int(zone_params.get('dmax', 0)) if zone_params else 0,
            })

    return events


# ==============================
# GÉNÉRATEURS XML
# ==============================

def generate_zombie_xml(zones):
    """Génère zombie_territories.xml. Désactivé → spawns = 0"""
    territories = {}
    for zone in zones:
        c = zone['color']
        if c not in territories:
            territories[c] = []
        territories[c].append(zone)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<territory-type>']
    for color, zlist in territories.items():
        lines.append(f'    <territory color="{color}">')
        for z in zlist:
            smin, smax = (z['smin'], z['smax']) if z['active'] else (0, 0)
            dmin, dmax = (z['dmin'], z['dmax']) if z['active'] else (0, 0)
            lines.append(
                f'        <zone name="{z["name"]}" '
                f'smin="{smin}" smax="{smax}" '
                f'dmin="{dmin}" dmax="{dmax}" '
                f'x="{z["x"]:.2f}" z="{z["z"]:.2f}" r="{z["r"]:.2f}"/>'
            )
        lines.append('    </territory>')
    lines.append('</territory-type>')
    return '\n'.join(lines)


def generate_event_spawns_xml(events):
    """
    Génère cfgeventspawns.xml.
    Regroupe par event name, conserve attributs bruts et ordre des positions.
    Désactivé (tous points inactifs) → zone params à 0.
    """
    grouped = {}
    order = []
    for ev in events:
        name = ev['name']
        if name not in grouped:
            grouped[name] = []
            order.append(name)
        grouped[name].append(ev)

    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>', '<eventposdef>']

    for name in order:
        evs = grouped[name]
        lines.append(f'\t<event name="{name}">')

        zone_params = evs[0].get('zone_params')
        if zone_params is not None:
            all_inactive = all(not e['active'] for e in evs)
            zp = {k: '0' for k in zone_params} if all_inactive else zone_params.copy()
            attrs_str = ' '.join(f'{k}="{v}"' for k, v in zp.items())
            lines.append(f'\t\t<zone {attrs_str} />')

        for ev in sorted(evs, key=lambda e: e['pos_index']):
            attrs_str = ' '.join(f'{k}="{v}"' for k, v in ev['pos_attrs'].items())
            lines.append(f'\t\t<pos {attrs_str}/>')

        lines.append('\t</event>')

    lines.append('</eventposdef>')
    return '\n'.join(lines)


# ==============================
# HELPERS
# ==============================

def load_image_b64(img_path):
    try:
        img = Image.open(img_path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def apply_offsets(points, map_key):
    offsets = MAP_CONFIG[map_key]['offsets']
    result = []
    for p in points:
        pc = p.copy()
        pc['x_plot'] = p['x'] + offsets['x']
        pc['y_plot'] = p['z'] + offsets['z']
        result.append(pc)
    return result


def parse_player_spawns(xml_content):
    """
    Parse cfgplayerspawnpoints.xml.
    3 types : fresh (nouveau spawn), hop (respawn rapide), travel (usage avancé).
    Nom du point = 'type|NomGroupe' pour portage couleur + filtre.
    """
    root = ET.fromstring(xml_content)
    points = []

    SPAWN_TYPES = {
        'fresh':  ('fresh',  True),   # (type, actif par défaut)
        'hop':    ('hop',    True),
        'travel': ('travel', False),  # désactivé par défaut — usage avancé
    }

    for spawn_type, (type_key, default_active) in SPAWN_TYPES.items():
        section = root.find(spawn_type)
        if section is None:
            continue
        bubbles = section.find('generator_posbubbles')
        if bubbles is None:
            continue
        for group in bubbles.findall('group'):
            group_name = group.get('name', 'Unknown')
            for i, pos in enumerate(group.findall('pos')):
                try:
                    x = float(pos.get('x', 0))
                    z = float(pos.get('z', 0))
                except ValueError:
                    continue
                points.append({
                    'source':     'spawns',
                    'name':       f"{type_key}|{group_name}",
                    'spawn_type': type_key,
                    'group':      group_name,
                    'x':          x,
                    'z':          z,
                    'pos_index':  i,
                    'active':     default_active,
                    # Pas de smin/smax pour les spawns joueurs
                })
    return points


def generate_player_spawns_xml(points):
    """
    Reconstruit cfgplayerspawnpoints.xml depuis la liste de points.
    Conserve la structure originale avec spawn_params et generator_params
    en les relisant depuis le fichier vanilla (lecture seule).
    Les positions désactivées sont simplement omises du fichier.
    """
    # Regrouper par type puis par groupe
    from collections import defaultdict
    by_type = defaultdict(lambda: defaultdict(list))
    for p in points:
        if p['active']:
            by_type[p['spawn_type']][p['group']].append(p)

    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>', '<playerspawnpoints>']

    TYPE_ORDER = ['fresh', 'hop', 'travel']
    for spawn_type in TYPE_ORDER:
        groups = by_type.get(spawn_type, {})
        lines.append(f'    <{spawn_type}>')
        lines.append(f'        <generator_posbubbles>')
        for group_name, pts in sorted(groups.items()):
            lines.append(f'            <group name="{group_name}">')
            for p in sorted(pts, key=lambda x: x['pos_index']):
                lines.append(f'                <pos x="{p["x"]}" z="{p["z"]}" />')
            lines.append(f'            </group>')
        lines.append(f'        </generator_posbubbles>')
        lines.append(f'    </{spawn_type}>')

    lines.append('</playerspawnpoints>')
    return '\n'.join(lines)


def load_from_file(map_key, data_type):
    filename = MAP_CONFIG[map_key]['files'][data_type]
    path = Path(__file__).parent.parent / "data" / filename
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if data_type == 'zombies':
        return parse_zombie_territories(content)
    elif data_type == 'spawns':
        return parse_player_spawns(content)
    else:
        return parse_event_spawns(content)


def sk(map_key, data_type):
    return f"data_{map_key}_{data_type}"


# ==============================
# CRÉATION CARTE PLOTLY
# ==============================

def create_map(points, map_key, selected_names, show_active_only):
    cfg = MAP_CONFIG[map_key]
    map_size = cfg['size']

    pts = apply_offsets(points, map_key)

    display = [
        (i, p) for i, p in enumerate(pts)
        if p['name'] in selected_names
        and (not show_active_only or p['active'])
    ]

    fig = go.Figure()

    # Image de fond
    img_b64 = load_image_b64(Path(__file__).parent.parent / "images" / cfg['image'])
    if img_b64:
        fig.add_layout_image(dict(
            source=f"data:image/png;base64,{img_b64}",
            xref="x", yref="y",
            x=0, y=map_size,
            sizex=map_size, sizey=map_size,
            sizing="stretch", opacity=0.75, layer="below"
        ))

    # Grouper par nom
    groups = defaultdict(list)
    for real_idx, p in display:
        groups[p['name']].append((real_idx, p))

    for point_name, items in sorted(groups.items()):
        real_indices = [i for i, _ in items]
        pts_g = [p for _, p in items]

        colors = [
            get_point_color(p['name'], p.get('source', 'zombies')) if p['active'] else '#444444'
            for p in pts_g
        ]

        hover_texts = []
        for p in pts_g:
            status = '✅ ACTIF' if p['active'] else '❌ INACTIF'
            if p.get('source') == 'zombies':
                hover_texts.append(
                    f"<b>{p['name']}</b><br>"
                    f"Position: ({p['x']:.0f}, {p['z']:.0f})<br>"
                    f"Radius: {p['r']:.0f}m<br>"
                    f"Spawn fixe: {p['smin']}–{p['smax']}<br>"
                    f"Spawn dyn: {p['dmin']}–{p['dmax']}<br>{status}"
                )
            elif p.get('source') == 'spawns':
                spawn_type = p.get('spawn_type', 'fresh')
                warning = '<br>⚠️ <i>Travel — usage avancé</i>' if spawn_type == 'travel' else ''
                hover_texts.append(
                    f"<b>{p['group']}</b><br>"
                    f"Type : {spawn_type.upper()}<br>"
                    f"Position: ({p['x']:.0f}, {p['z']:.0f})"
                    f"{warning}<br>{status}"
                )
            else:
                cat = p.get('category', '❓')
                extra = ''
                if p.get('zone_params'):
                    zp = p['zone_params']
                    extra = f"<br>Zone: smin={zp.get('smin',0)} smax={zp.get('smax',0)} r={zp.get('r',0)}m"
                if p['pos_attrs'].get('group'):
                    extra += f"<br>Groupe: {p['pos_attrs']['group']}"
                hover_texts.append(
                    f"<b>{p['name']}</b><br>"
                    f"Catégorie: {cat}<br>"
                    f"Position: ({p['x']:.0f}, {p['z']:.0f})"
                    f"{extra}<br>{status}"
                )

        fig.add_trace(go.Scatter(
            x=[p['x_plot'] for p in pts_g],
            y=[p['y_plot'] for p in pts_g],
            mode='markers',
            name=point_name,
            marker=dict(size=10, sizemin=5, color=colors, opacity=0.9,
                        line=dict(width=1, color='white')),
            text=hover_texts,
            hovertemplate='%{text}<extra></extra>',
            customdata=real_indices,
            selected=dict(marker=dict(size=14, color='#FFD700')),
            unselected=dict(marker=dict(opacity=0.5))
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>{map_key.capitalize()}</b> — {len(display)} points affichés",
            font=dict(color='#00D4FF', size=16)
        ),
        height=800,
        hovermode='closest',
        dragmode='pan',
        legend=dict(
            yanchor="top", y=0.99, xanchor="right", x=0.99,
            bgcolor="rgba(15, 20, 40, 0.92)",
            bordercolor="#00D4FF", borderwidth=1,
            font=dict(color='white', size=11)
        ),
        xaxis=dict(range=[0, map_size], showgrid=False, zeroline=False,
                   showticklabels=False, fixedrange=False),
        yaxis=dict(range=[0, map_size], scaleanchor="x", scaleratio=1,
                   showgrid=False, zeroline=False, showticklabels=False, fixedrange=False),
        plot_bgcolor='#0a0a1a',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        uirevision=map_key
    )

    return fig, len(display)


# ==============================
# SESSION STATE INIT
# ==============================
for mk in MAP_CONFIG:
    for dt in ('zombies', 'events', 'spawns'):
        key = sk(mk, dt)
        if key not in st.session_state:
            try:
                st.session_state[key] = load_from_file(mk, dt)
            except Exception:
                st.session_state[key] = []

if 'sel_idx'    not in st.session_state: st.session_state.sel_idx    = None
if 'sel_map'    not in st.session_state: st.session_state.sel_map    = None
if 'sel_source' not in st.session_state: st.session_state.sel_source = None

# ==============================
# HEADER
# ==============================
# Header image
try:
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.image("assets/images/codex_header.png", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception:
    pass

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="page-title">🗺️ Carte Interactive — DayZ</div>', unsafe_allow_html=True)

if st.button("⬅️ Retour à l\'accueil"):
    st.switch_page("app.py")

st.markdown("""
<div class="calibration-note">
    📍 <b>Calibration :</b>
    ✅ Chernarus (15 360u) &nbsp;|&nbsp;
    ✅ Livonia (12 800u) &nbsp;|&nbsp;
    ✅ Sakhal (15 360u)<br>
    🖱️ <b>Navigation :</b> Molette = Zoom &nbsp;·&nbsp; Clic gauche maintenu = Déplacement &nbsp;·&nbsp; Double-clic = Reset vue
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# TABS CARTES
# ==============================
tabs = st.tabs([MAP_CONFIG[mk]['label'] for mk in MAP_CONFIG])

for tab_obj, map_key in zip(tabs, MAP_CONFIG):
    with tab_obj:

        # --- Sélecteur type d'événement ---
        st.markdown("### 🎯 Type d'événement")
        event_mode = st.radio(
            "Afficher sur la carte :",
            options=['🧟 Zombies', '📍 Events (véhicules, crashes, gaz...)', '👤 Spawns joueurs'],
            horizontal=True,
            key=f"mode_{map_key}"
        )
        is_zombie_mode  = event_mode.startswith('🧟')
        is_spawns_mode  = event_mode.startswith('👤')
        if is_zombie_mode:
            data_type = 'zombies'
        elif is_spawns_mode:
            data_type = 'spawns'
        else:
            data_type = 'events'
        data_key = sk(map_key, data_type)
        points = st.session_state[data_key]

        st.markdown("---")

        # --- Stats ---
        active_pts = [p for p in points if p['active']]
        names_all = sorted(set(p['name'] for p in points))

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="stats-box"><h2>{len(points)}</h2><p>Points totaux</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="stats-box"><h2>{len(active_pts)}</h2><p>✅ Actifs</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="stats-box"><h2>{len(names_all)}</h2><p>Types</p></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="stats-box"><h2>{len(points)-len(active_pts)}</h2><p>❌ Inactifs</p></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- Filtres ---
        col_f1, col_f2 = st.columns([3, 1])
        with col_f1:
            if is_zombie_mode:
                selected_names = st.multiselect(
                    "🔍 Filtrer par type de zombie",
                    names_all, default=names_all,
                    key=f"filter_{map_key}_{data_type}"
                )
            elif is_spawns_mode:
                # Filtre par type de spawn
                spawn_types_avail = sorted(set(p.get('spawn_type', 'fresh') for p in points))
                selected_spawn_types = st.multiselect(
                    "🔍 Filtrer par type de spawn",
                    spawn_types_avail,
                    default=[t for t in spawn_types_avail if t != 'travel'],  # travel masqué par défaut
                    key=f"filter_spawn_{map_key}"
                )
                if 'travel' in selected_spawn_types:
                    st.warning("⚠️ **Travel** — zones de spawn avancées. À modifier uniquement si vous savez ce que vous faites.")
                selected_names = sorted(set(
                    p['name'] for p in points
                    if p.get('spawn_type', 'fresh') in selected_spawn_types
                ))
            else:
                # Filtre par catégorie events
                cats_available = sorted(set(p.get('category', '❓ Autre') for p in points))
                selected_cats = st.multiselect(
                    "🔍 Filtrer par catégorie",
                    cats_available, default=cats_available,
                    key=f"filter_cat_{map_key}"
                )
                selected_names = sorted(set(
                    p['name'] for p in points
                    if p.get('category', '❓ Autre') in selected_cats
                ))
        with col_f2:
            show_active_only = st.checkbox(
                "Actifs seulement", value=False,
                key=f"active_only_{map_key}_{data_type}"
            )

        # --- Carte ---
        fig, displayed = create_map(points, map_key, selected_names, show_active_only)
        st.caption(f"📊 {displayed} points affichés sur {len(points)} totaux")

        sel_data = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            key=f"map_{map_key}_{data_type}",
            config={
                'scrollZoom': True,
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoScale2d'],
                'doubleClick': 'reset',
                'toImageButtonOptions': {'format': 'png', 'filename': f'carte_{map_key}'}
            }
        )

        if (sel_data
                and 'selection' in sel_data
                and sel_data['selection'].get('points')):
            pt = sel_data['selection']['points'][0]
            st.session_state.sel_idx    = pt['customdata']
            st.session_state.sel_map    = map_key
            st.session_state.sel_source = data_type

        st.markdown("---")

        # --- Actions rapides ---
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            if st.button("✅ Tout activer", key=f"on_{map_key}_{data_type}", use_container_width=True):
                for p in points: p['active'] = True
                st.session_state.sel_idx = None
                st.rerun()
        with col_a2:
            if st.button("❌ Tout désactiver", key=f"off_{map_key}_{data_type}", use_container_width=True):
                for p in points: p['active'] = False
                st.session_state.sel_idx = None
                st.rerun()
        with col_a3:
            if st.button("🔄 Réinitialiser (vanilla)", key=f"reset_{map_key}_{data_type}", use_container_width=True):
                try:
                    st.session_state[data_key] = load_from_file(map_key, data_type)
                    st.session_state.sel_idx = None
                    st.success("Configuration vanilla rechargée !")
                    st.rerun()
                except Exception:
                    st.error("Fichier introuvable dans data/")

        st.markdown("---")

        # --- Export ---
        if is_zombie_mode:
            xml_out = generate_zombie_xml(points)
        elif is_spawns_mode:
            xml_out = generate_player_spawns_xml(points)
        else:
            xml_out = generate_event_spawns_xml(points)
        fname = MAP_CONFIG[map_key]['files'][data_type]

        st.download_button(
            label=f"📥 Exporter {fname}",
            data=xml_out,
            file_name=fname,
            mime="text/xml",
            use_container_width=True,
            type="primary",
            key=f"dl_{map_key}_{data_type}"
        )


# ==============================
# PANNEAU D'ÉDITION (GLOBAL)
# ==============================
if (st.session_state.sel_idx is not None
        and st.session_state.sel_map is not None
        and st.session_state.sel_source is not None):

    map_key   = st.session_state.sel_map
    zone_idx  = st.session_state.sel_idx
    data_type = st.session_state.sel_source
    data_key  = sk(map_key, data_type)
    points    = st.session_state[data_key]

    if zone_idx < len(points):
        point = points[zone_idx]

        st.markdown("---")
        st.markdown(f"### ✏️ Édition — {map_key.capitalize()} / {point['name']}")

        col_card, col_toggle = st.columns([3, 1])

        with col_card:
            status_str = '✅ ACTIF' if point['active'] else '❌ INACTIF'
            if data_type == 'zombies':
                details = (
                    f"<p>📍 Position : ({point['x']:.1f}, {point['z']:.1f}) &nbsp;|&nbsp; Radius : {point['r']:.0f}m</p>"
                    f"<p>Spawn fixe : {point['smin']}–{point['smax']} &nbsp;|&nbsp; Spawn dyn : {point['dmin']}–{point['dmax']}</p>"
                )
            elif data_type == 'spawns':
                spawn_type = point.get('spawn_type', 'fresh')
                travel_warn = ' &nbsp;⚠️ <i>Usage avancé</i>' if spawn_type == 'travel' else ''
                details = (
                    f"<p>📍 Position : ({point['x']:.1f}, {point['z']:.1f})</p>"
                    f"<p>Type : <b>{spawn_type.upper()}</b>{travel_warn} &nbsp;|&nbsp; Groupe : {point.get('group','?')}</p>"
                )
            else:
                cat = point.get('category', '❓')
                group_info = f" &nbsp;|&nbsp; Groupe : {point['pos_attrs']['group']}" if point['pos_attrs'].get('group') else ''
                details = (
                    f"<p>📍 Position : ({point['x']:.1f}, {point['z']:.1f}){group_info}</p>"
                    f"<p>Catégorie : {cat}</p>"
                )
            st.markdown(f"""
            <div class="zone-card">
                <h4>{point['name']}</h4>
                {details}
                <p>Statut : <b>{status_str}</b></p>
            </div>
            """, unsafe_allow_html=True)

        with col_toggle:
            st.markdown("<br>", unsafe_allow_html=True)
            new_active = st.toggle(
                "Point actif",
                value=point['active'],
                key=f"toggle_{map_key}_{data_type}_{zone_idx}",
                help="Si désactivé → spawns = 0 dans le fichier exporté"
            )
            if new_active != point['active']:
                points[zone_idx]['active'] = new_active
                st.rerun()

        # Édition spawns — zombies uniquement
        if data_type == 'zombies':
            st.markdown('<div class="tip-box">💡 Modifie les valeurs et clique <b>Sauvegarder</b>. Si désactivé, les spawns seront à 0 à l\'export.</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1: new_smin = st.number_input("smin", value=point['smin'], min_value=0, max_value=100, key=f"smin_{map_key}_{zone_idx}")
            with c2: new_smax = st.number_input("smax", value=point['smax'], min_value=0, max_value=100, key=f"smax_{map_key}_{zone_idx}")
            with c3: new_dmin = st.number_input("dmin", value=point['dmin'], min_value=0, max_value=100, key=f"dmin_{map_key}_{zone_idx}")
            with c4: new_dmax = st.number_input("dmax", value=point['dmax'], min_value=0, max_value=100, key=f"dmax_{map_key}_{zone_idx}")

            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("💾 Sauvegarder", type="primary", use_container_width=True, key=f"save_{map_key}_{zone_idx}"):
                    if new_smin > new_smax:
                        st.error("⚠️ smin ne peut pas être > smax !")
                    elif new_dmin > new_dmax:
                        st.error("⚠️ dmin ne peut pas être > dmax !")
                    else:
                        points[zone_idx].update({'smin': new_smin, 'smax': new_smax, 'dmin': new_dmin, 'dmax': new_dmax})
                        st.session_state.sel_idx = None
                        st.success(f"✅ Zone '{point['name']}' mise à jour !")
                        st.rerun()
            with cb2:
                if st.button("✖️ Fermer", use_container_width=True, key=f"close_{map_key}_{zone_idx}"):
                    st.session_state.sel_idx = None
                    st.rerun()
        elif data_type == 'spawns':
            spawn_type = point.get('spawn_type', 'fresh')
            if spawn_type == 'travel':
                st.warning("⚠️ **Point Travel** — zone de spawn avancée. Si désactivé, ce point sera exclu de l\'export.")
            else:
                st.markdown('<div class="tip-box">💡 Active/désactive ce point de spawn. Les points désactivés sont exclus de l\'export XML.</div>', unsafe_allow_html=True)
            if st.button("✖️ Fermer", use_container_width=True, key=f"close_sp_{map_key}_{zone_idx}"):
                st.session_state.sel_idx = None
                st.rerun()
        else:
            st.markdown('<div class="tip-box">💡 En mode Events, tu peux activer/désactiver les positions.</div>', unsafe_allow_html=True)
            if st.button("✖️ Fermer", use_container_width=True, key=f"close_ev_{map_key}_{zone_idx}"):
                st.session_state.sel_idx = None
                st.rerun()
