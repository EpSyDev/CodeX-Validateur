"""
Codex Suite - Carte Interactive
Éditeur visuel des spawns zombies - Chernarus, Livonia, Sakhal

🎯 VERSION REFONTE ERGONOMIE :
- Zoom molette natif Plotly (suppression encart navigation)
- Pan clic gauche natif optimisé
- Markers avec taille minimale au zoom (sizemin)
- Fix bug édition Chernarus/Livonia (customdata = vrai index zones_list)
- Désactivation → smin/smax/dmin/dmax = 0 dans le XML
- Sauvegarde auto session_state, export manuel
- Interface édition claire et directe
"""

import streamlit as st
import xml.etree.ElementTree as ET
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex - Carte Interactive",
    page_icon="🗺️",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.zone-card {
    background: #1a1a2e;
    color: #e0e0e0;
    padding: 15px 20px;
    border-radius: 10px;
    border-left: 4px solid #00D4FF;
    margin: 10px 0;
}
.zone-card h4 { color: #00D4FF; margin: 0 0 8px 0; }
.zone-card p { margin: 4px 0; font-size: 0.9em; }

.stats-box {
    background: linear-gradient(135deg, #0f3460, #16213e);
    color: white;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #00D4FF33;
    margin: 6px 0;
}
.stats-box h2 { color: #00D4FF; margin: 0; font-size: 2em; }
.stats-box p { margin: 4px 0 0 0; font-size: 0.85em; color: #aaa; }

.calibration-note {
    background: #1a2a1a;
    border-left: 4px solid #00D4FF;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 4px;
    color: #ccc;
    font-size: 0.9em;
}

.edit-panel {
    background: #16213e;
    border: 1px solid #00D4FF44;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
}

.tip-box {
    background: #0f2027;
    border-left: 3px solid #ffc107;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.85em;
    color: #ccc;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# CONFIG CARTES
# ==============================
MAP_CONFIG = {
    'chernarus': {
        'label': '🗺️ Chernarus ✅',
        'size': 15360,
        'image': 'chernarus_map.jpg',
        'session_key': 'zones_chernarus',
        'xml_file': 'zombie_territories_chernarus.xml',
        'offsets': {'x': 0, 'z': 0}
    },
    'livonia': {
        'label': '🗺️ Livonia ✅',
        'size': 12800,
        'image': 'livonia_map.jpg',
        'session_key': 'zones_livonia',
        'xml_file': 'zombie_territories_livonia.xml',
        'offsets': {'x': 0, 'z': 0}
    },
    'sakhal': {
        'label': '🗺️ Sakhal ✅',
        'size': 15360,
        'image': 'sakhal_map.webp',
        'session_key': 'zones_sakhal',
        'xml_file': 'zombie_territories_sakhal.xml',
        'offsets': {'x': 0, 'z': -21}
    }
}

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

# ==============================
# FONCTIONS HELPERS
# ==============================

def parse_zombie_territories(xml_content):
    """Parse zombie_territories.xml → liste de zones avec index original"""
    root = ET.fromstring(xml_content)
    zones = []
    for territory in root.findall('territory'):
        color = territory.get('color', '')
        for zone in territory.findall('zone'):
            zones.append({
                'name':   zone.get('name'),
                'x':      float(zone.get('x')),
                'z':      float(zone.get('z')),
                'r':      float(zone.get('r')),
                'smin':   int(zone.get('smin')),
                'smax':   int(zone.get('smax')),
                'dmin':   int(zone.get('dmin')),
                'dmax':   int(zone.get('dmax')),
                # Valeurs originales conservées pour reset
                'smin_orig': int(zone.get('smin')),
                'smax_orig': int(zone.get('smax')),
                'dmin_orig': int(zone.get('dmin')),
                'dmax_orig': int(zone.get('dmax')),
                'color':  color,
                'active': True,
            })
    return zones


def get_zone_color(zone_name):
    for key, color in ZOMBIE_COLORS.items():
        if key in zone_name:
            return color
    return '#808080'


def apply_map_offsets(zones, map_key):
    """Applique les offsets de calibration iZurvive — retourne une copie"""
    offsets = MAP_CONFIG[map_key]['offsets']
    result = []
    for zone in zones:
        z = zone.copy()
        z['x_plot'] = zone['x'] + offsets['x']
        z['y_plot'] = zone['z'] + offsets['z']
        result.append(z)
    return result


def generate_xml(zones):
    """
    Génère le XML depuis la liste de zones.
    Règle : si active=False → smin/smax/dmin/dmax = 0 dans le fichier
    Les coordonnées et le radius ne changent jamais.
    """
    territories = {}
    for zone in zones:
        color = zone['color']
        if color not in territories:
            territories[color] = []
        territories[color].append(zone)

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<territory-type>')

    for color, zones_list in territories.items():
        xml_lines.append(f'    <territory color="{color}">')
        for zone in zones_list:
            # Si désactivé → tous les spawns à 0
            if zone['active']:
                smin, smax = zone['smin'], zone['smax']
                dmin, dmax = zone['dmin'], zone['dmax']
            else:
                smin = smax = dmin = dmax = 0

            xml_lines.append(
                f'        <zone name="{zone["name"]}" '
                f'smin="{smin}" smax="{smax}" '
                f'dmin="{dmin}" dmax="{dmax}" '
                f'x="{zone["x"]:.2f}" z="{zone["z"]:.2f}" r="{zone["r"]:.2f}"/>'
            )
        xml_lines.append('    </territory>')

    xml_lines.append('</territory-type>')
    return '\n'.join(xml_lines)


def load_image_b64(img_path):
    """Charge une image et la convertit en base64 pour Plotly"""
    try:
        img = Image.open(img_path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return None


def create_map(zones_data, map_key, selected_types, show_active_only):
    """
    Crée la figure Plotly pour une carte.
    
    ✅ Fixes :
    - customdata = index réel dans zones_data (pas index DataFrame)
    - sizemin=5 pour éviter disparition au zoom
    - Zoom molette + pan natifs Plotly (pas d'encart)
    - Markers inactifs en gris avec opacité réduite
    """
    cfg = MAP_CONFIG[map_key]
    map_size = cfg['size']

    # Appliquer offsets de calibration
    zones_plotted = apply_map_offsets(zones_data, map_key)

    # Filtrer pour l'affichage (on garde l'index réel dans zones_data)
    display = [
        (i, z) for i, z in enumerate(zones_plotted)
        if z['name'] in selected_types
        and (not show_active_only or z['active'])
    ]

    fig = go.Figure()

    # Image de fond
    img_path = Path(__file__).parent.parent / "images" / cfg['image']
    img_b64 = load_image_b64(img_path)
    if img_b64:
        fig.add_layout_image(dict(
            source=f"data:image/png;base64,{img_b64}",
            xref="x", yref="y",
            x=0, y=map_size,
            sizex=map_size, sizey=map_size,
            sizing="stretch",
            opacity=0.75,
            layer="below"
        ))
    else:
        st.warning(f"⚠️ Image de fond introuvable : {cfg['image']}")

    # Grouper par type de zombie pour la légende
    from collections import defaultdict
    groups = defaultdict(list)
    for real_idx, z in display:
        groups[z['name']].append((real_idx, z))

    for zone_type, items in sorted(groups.items()):
        real_indices = [i for i, _ in items]
        zs = [z for _, z in items]

        # Couleur : gris si inactif, couleur normale si actif
        colors = [
            get_zone_color(z['name']) if z['active'] else '#555555'
            for z in zs
        ]
        opacities_marker = [0.9 if z['active'] else 0.4 for z in zs]

        hover_texts = []
        for z in zs:
            status = '✅ ACTIF' if z['active'] else '❌ INACTIF (spawns = 0 en export)'
            hover_texts.append(
                f"<b>{z['name']}</b><br>"
                f"Position: ({z['x']:.0f}, {z['z']:.0f})<br>"
                f"Radius: {z['r']:.0f}m<br>"
                f"Spawn fixe: {z['smin']}–{z['smax']}<br>"
                f"Spawn dyn: {z['dmin']}–{z['dmax']}<br>"
                f"{status}"
            )

        fig.add_trace(go.Scatter(
            x=[z['x_plot'] for z in zs],
            y=[z['y_plot'] for z in zs],
            mode='markers',
            name=zone_type,
            marker=dict(
                size=10,
                sizemin=5,          # Taille minimale même au dézoom total
                color=colors,
                opacity=0.9,
                line=dict(width=1, color='white')
            ),
            text=hover_texts,
            hovertemplate='%{text}<extra></extra>',
            # ✅ FIX CRITIQUE : on stocke l'index RÉEL dans zones_data
            customdata=real_indices,
            selected=dict(marker=dict(size=14, color='#FFD700')),
            unselected=dict(marker=dict(opacity=0.5))
        ))

    map_name = map_key.capitalize()
    fig.update_layout(
        title=dict(
            text=f"<b>{map_name}</b> — Zones de spawn zombies | "
                 f"{len(display)} zones affichées",
            font=dict(color='#00D4FF', size=16)
        ),
        height=800,
        hovermode='closest',
        # ✅ Zoom molette natif + pan clic gauche (dragmode par défaut)
        dragmode='pan',
        legend=dict(
            yanchor="top", y=0.99,
            xanchor="right", x=0.99,
            bgcolor="rgba(15, 20, 40, 0.92)",
            bordercolor="#00D4FF",
            borderwidth=1,
            font=dict(color='white', size=11)
        ),
        xaxis=dict(
            range=[0, map_size],
            showgrid=False, zeroline=False, showticklabels=False,
            fixedrange=False   # Permettre zoom sur axe X
        ),
        yaxis=dict(
            range=[0, map_size],
            scaleanchor="x", scaleratio=1,
            showgrid=False, zeroline=False, showticklabels=False,
            fixedrange=False   # Permettre zoom sur axe Y
        ),
        plot_bgcolor='#0a0a1a',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        # ✅ Activer scroll wheel zoom
        uirevision=map_key   # Préserve le zoom entre reruns Streamlit
    )

    return fig, len(display)


def load_zones_from_file(map_key):
    """Charge les zones depuis le fichier XML vanilla"""
    cfg = MAP_CONFIG[map_key]
    path = Path(__file__).parent.parent / "data" / cfg['xml_file']
    with open(path, 'r', encoding='utf-8') as f:
        return parse_zombie_territories(f.read())


# ==============================
# SESSION STATE INIT
# ==============================
for mk in MAP_CONFIG:
    sk = MAP_CONFIG[mk]['session_key']
    if sk not in st.session_state:
        try:
            st.session_state[sk] = load_zones_from_file(mk)
        except Exception as e:
            st.session_state[sk] = []

if 'selected_zone_idx' not in st.session_state:
    st.session_state.selected_zone_idx = None

if 'selected_map_key' not in st.session_state:
    st.session_state.selected_map_key = None

# ==============================
# HEADER
# ==============================
try:
    st.image("assets/images/codex_header1.png", use_column_width=True)
except Exception:
    pass

st.title("🗺️ Carte Interactive — DayZ")
st.subheader("Éditeur visuel des spawns zombies")

if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

st.markdown("""
<div class="calibration-note">
    📍 <b>Calibration :</b>
    ✅ Chernarus (15 360u) &nbsp;|&nbsp;
    ✅ Livonia (12 800u) &nbsp;|&nbsp;
    ✅ Sakhal (12 800u)<br>
    🖱️ <b>Navigation :</b> Molette = Zoom · Clic gauche maintenu = Déplacement · Double-clic = Reset vue
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# TABS
# ==============================
tabs = st.tabs([MAP_CONFIG[mk]['label'] for mk in MAP_CONFIG])

for tab_obj, map_key in zip(tabs, MAP_CONFIG):
    with tab_obj:
        cfg = MAP_CONFIG[map_key]
        sk = cfg['session_key']
        zones = st.session_state[sk]

        # --- Stats ---
        active_zones = [z for z in zones if z['active']]
        zone_types_all = sorted(set(z['name'] for z in zones))
        inactive_count = len(zones) - len(active_zones)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="stats-box"><h2>{len(zones)}</h2><p>Zones totales</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="stats-box"><h2>{len(active_zones)}</h2><p>✅ Actives</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="stats-box"><h2>{len(zone_types_all)}</h2><p>Types</p></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="stats-box"><h2>{inactive_count}</h2><p>❌ Inactives</p></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- Filtres ---
        col_f1, col_f2 = st.columns([3, 1])
        with col_f1:
            selected_types = st.multiselect(
                "🔍 Filtrer par type de zombie",
                zone_types_all,
                default=zone_types_all,
                key=f"filter_{map_key}"
            )
        with col_f2:
            show_active_only = st.checkbox(
                "Actives seulement",
                value=False,
                key=f"active_only_{map_key}"
            )

        # --- Carte ---
        fig, displayed_count = create_map(zones, map_key, selected_types, show_active_only)
        st.caption(f"📊 {displayed_count} zones affichées sur {len(zones)} totales")

        selected_data = st.plotly_chart(
            fig,
            use_container_width=True,
            on_select="rerun",
            key=f"map_{map_key}",
            config={
                'scrollZoom': True,          # ✅ Zoom molette activé
                'displayModeBar': True,
                'modeBarButtonsToRemove': [
                    'select2d', 'lasso2d', 'autoScale2d'
                ],
                'modeBarButtonsToAdd': [],
                'doubleClick': 'reset',      # Double-clic reset vue
                'toImageButtonOptions': {'format': 'png', 'filename': f'carte_{map_key}'}
            }
        )

        # Récupérer la sélection
        if (selected_data
                and 'selection' in selected_data
                and 'points' in selected_data['selection']
                and selected_data['selection']['points']):
            point = selected_data['selection']['points'][0]
            real_idx = point['customdata']   # ✅ Index réel dans zones_list
            st.session_state.selected_zone_idx = real_idx
            st.session_state.selected_map_key = map_key

        st.markdown("---")

        # --- Actions rapides ---
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            if st.button("✅ Tout activer", key=f"all_on_{map_key}", use_container_width=True):
                for z in zones:
                    z['active'] = True
                st.session_state.selected_zone_idx = None
                st.rerun()
        with col_a2:
            if st.button("❌ Tout désactiver", key=f"all_off_{map_key}", use_container_width=True):
                for z in zones:
                    z['active'] = False
                st.session_state.selected_zone_idx = None
                st.rerun()
        with col_a3:
            if st.button("🔄 Réinitialiser (vanilla)", key=f"reset_{map_key}", use_container_width=True):
                try:
                    st.session_state[sk] = load_zones_from_file(map_key)
                    st.session_state.selected_zone_idx = None
                    st.success("Configuration vanilla rechargée !")
                    st.rerun()
                except Exception:
                    st.error("Fichier vanilla introuvable")

        st.markdown("---")

        # --- Export ---
        xml_content = generate_xml(zones)
        st.download_button(
            label=f"📥 Exporter zombie_territories_{map_key}.xml",
            data=xml_content,
            file_name=f"zombie_territories_{map_key}.xml",
            mime="text/xml",
            use_container_width=True,
            type="primary",
            key=f"dl_{map_key}"
        )

# ==============================
# PANNEAU D'ÉDITION (GLOBAL)
# Affiché en dehors des tabs pour être toujours visible
# ==============================
if st.session_state.selected_zone_idx is not None and st.session_state.selected_map_key is not None:
    map_key = st.session_state.selected_map_key
    zone_idx = st.session_state.selected_zone_idx
    sk = MAP_CONFIG[map_key]['session_key']
    zones = st.session_state[sk]

    if zone_idx < len(zones):
        zone = zones[zone_idx]
        map_name = map_key.capitalize()

        st.markdown("---")
        st.markdown(f"### ✏️ Édition — Zone sélectionnée ({map_name})")

        col_card, col_toggle = st.columns([3, 1])

        with col_card:
            status_str = '✅ ACTIF' if zone['active'] else '❌ INACTIF (spawns = 0 à l\'export)'
            st.markdown(f"""
            <div class="zone-card">
                <h4>{zone['name']}</h4>
                <p>📍 Position : ({zone['x']:.1f}, {zone['z']:.1f}) &nbsp;|&nbsp; Radius : {zone['r']:.0f}m</p>
                <p>Statut : <b>{status_str}</b></p>
            </div>
            """, unsafe_allow_html=True)

        with col_toggle:
            st.markdown("<br>", unsafe_allow_html=True)
            new_active = st.toggle(
                "Zone active",
                value=zone['active'],
                key=f"edit_toggle_{map_key}_{zone_idx}",
                help="Si désactivé → smin/smax/dmin/dmax = 0 dans le fichier exporté"
            )
            if new_active != zone['active']:
                zones[zone_idx]['active'] = new_active
                st.rerun()

        st.markdown('<div class="tip-box">💡 Modifie les valeurs et clique <b>Sauvegarder</b>. L\'export XML reflètera ces changements. Si la zone est désactivée, les spawns seront à 0 quel que soit le nombre saisi.</div>', unsafe_allow_html=True)

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            new_smin = st.number_input(
                "smin (spawn fixe min)",
                value=zone['smin'], min_value=0, max_value=100,
                key=f"edit_smin_{map_key}_{zone_idx}",
                help="Nombre minimum de zombies spawn fixe"
            )
        with col_s2:
            new_smax = st.number_input(
                "smax (spawn fixe max)",
                value=zone['smax'], min_value=0, max_value=100,
                key=f"edit_smax_{map_key}_{zone_idx}",
                help="Nombre maximum de zombies spawn fixe"
            )
        with col_s3:
            new_dmin = st.number_input(
                "dmin (spawn dyn min)",
                value=zone['dmin'], min_value=0, max_value=100,
                key=f"edit_dmin_{map_key}_{zone_idx}",
                help="Nombre minimum de zombies dynamiques"
            )
        with col_s4:
            new_dmax = st.number_input(
                "dmax (spawn dyn max)",
                value=zone['dmax'], min_value=0, max_value=100,
                key=f"edit_dmax_{map_key}_{zone_idx}",
                help="Nombre maximum de zombies dynamiques"
            )

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("💾 Sauvegarder", type="primary", use_container_width=True, key=f"save_{map_key}_{zone_idx}"):
                if new_smin > new_smax:
                    st.error("⚠️ smin ne peut pas être supérieur à smax !")
                elif new_dmin > new_dmax:
                    st.error("⚠️ dmin ne peut pas être supérieur à dmax !")
                else:
                    zones[zone_idx]['smin'] = new_smin
                    zones[zone_idx]['smax'] = new_smax
                    zones[zone_idx]['dmin'] = new_dmin
                    zones[zone_idx]['dmax'] = new_dmax
                    st.session_state.selected_zone_idx = None
                    st.success(f"✅ Zone '{zone['name']}' mise à jour !")
                    st.rerun()

        with col_btn2:
            if st.button("✖️ Fermer sans sauvegarder", use_container_width=True, key=f"close_edit_{map_key}_{zone_idx}"):
                st.session_state.selected_zone_idx = None
                st.rerun()
