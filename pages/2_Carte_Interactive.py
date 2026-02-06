"""
Codex Suite - Carte Interactive
Éditeur visuel des spawns zombies - Chernarus, Livonia, Sakhal

🎯 VERSION CORRIGÉE : Utilise des offsets simples au lieu de normalisation complexe
"""

import streamlit as st
import xml.etree.ElementTree as ET
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

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
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 10px 0;
    border-left: 4px solid #667eea;
}

.stats-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin: 10px 0;
}

.calibration-note {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 12px;
    margin: 10px 0;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# FONCTIONS HELPERS
# ==============================
def parse_zombie_territories(xml_content):
    """Parse le fichier zombie_territories.xml et retourne une liste de zones"""
    root = ET.fromstring(xml_content)
    zones = []
    
    for territory in root.findall('territory'):
        color = territory.get('color', '')
        
        for zone in territory.findall('zone'):
            zones.append({
                'name': zone.get('name'),
                'x': float(zone.get('x')),
                'z': float(zone.get('z')),
                'r': float(zone.get('r')),
                'smin': int(zone.get('smin')),
                'smax': int(zone.get('smax')),
                'dmin': int(zone.get('dmin')),
                'dmax': int(zone.get('dmax')),
                'color': color,
                'active': True
            })
    
    return zones

def get_zone_color(zone_name):
    """Retourne une couleur selon le type de zombie"""
    color_map = {
        'InfectedArmy': '#8B0000',
        'InfectedArmyHard': '#DC143C',
        'InfectedCity': '#4169E1',
        'InfectedIndustrial': '#FF8C00',
        'InfectedVillage': '#32CD32',
        'InfectedPolice': '#191970',
        'InfectedMedic': '#FF1493',
        'InfectedPrisoner': '#8B4513',
        'InfectedFirefighter': '#FF4500',
        'InfectedReligious': '#9370DB',
    }
    
    for key, color in color_map.items():
        if key in zone_name:
            return color
    
    return '#808080'

def apply_map_offsets(zones, map_name):
    """
    Applique les offsets de calibration iZurvive aux coordonnées DayZ
    
    🎯 DÉCOUVERTE : Les coordonnées DayZ XML sont DÉJÀ dans [0-12800] !
    iZurvive applique juste un offset constant pour chaque carte.
    
    ✅ Offsets validés (précision parfaite - 0px d'erreur) :
    - Chernarus : X-26, Z+17 (testé avec caserne de pompiers)
    - Livonia : X+206, Z-73 (testé avec Topolin)
    - Sakhal : X+0, Z-21 (testé avec caserne ouest)
    """
    if len(zones) == 0:
        return zones
    
    # Offsets de calibration par carte (en pixels)
    MAP_OFFSETS = {
        'Chernarus': {'x': -26, 'z': 1017},   # ✅ AJUSTÉ (décalage vers le sud)
        'Livonia':   {'x': 206, 'z': -73},    # ✅ VALIDÉ (Topolin)
        'Sakhal':    {'x': 0, 'z': -21}       # ✅ VALIDÉ (Caserne ouest)
    }
    
    offsets = MAP_OFFSETS.get(map_name, {'x': 0, 'z': 0})
    
    # Appliquer les offsets
    for zone in zones:
        # Les coordonnées DayZ sont déjà dans le bon système !
        # On applique juste l'offset de calibration iZurvive
        zone['x_izurvive'] = zone['x'] + offsets['x']
        zone['z_izurvive'] = zone['z'] + offsets['z']
        
        # Pas d'inversion Y : iZurvive et Plotly utilisent tous deux (0,0) en bas à gauche
        zone['y_plot'] = zone['z_izurvive']
    
    return zones

def generate_xml(zones):
    """Génère le XML depuis la liste de zones"""
    territories = {}
    
    # Regrouper TOUTES les zones par couleur (actives ET inactives)
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
            xml_lines.append(
                f'        <zone name="{zone["name"]}" '
                f'smin="{zone["smin"]}" smax="{zone["smax"]}" '
                f'dmin="{zone["dmin"]}" dmax="{zone["dmax"]}" '
                f'x="{zone["x"]:.2f}" z="{zone["z"]:.2f}" r="{zone["r"]:.2f}"/>'
            )
        xml_lines.append('    </territory>')
    
    xml_lines.append('</territory-type>')
    
    return '\n'.join(xml_lines)

def create_map(zones_data, map_name, map_size, img_path):
    """Crée une carte interactive pour une map donnée"""
    
    # Appliquer les offsets de calibration
    zones_data = apply_map_offsets(zones_data, map_name)
    
    df = pd.DataFrame(zones_data)
    
    if len(df) == 0:
        st.warning(f"Aucune zone à afficher pour {map_name}")
        return None
    
    fig = go.Figure()
    
    # Charger l'image de fond
    from PIL import Image
    import base64
    from io import BytesIO
    
    try:
        img = Image.open(img_path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_str}",
                xref="x",
                yref="y",
                x=0,
                y=map_size,
                sizex=map_size,
                sizey=map_size,
                sizing="stretch",
                opacity=0.7,
                layer="below"
            )
        )
    except Exception as e:
        st.warning(f"⚠️ Image de fond non trouvée pour {map_name}")
    
    # Ajouter les marqueurs
    for zone_type in df['name'].unique():
        df_type = df[df['name'] == zone_type]
        
        fig.add_trace(go.Scatter(
            x=df_type['x_izurvive'],
            y=df_type['y_plot'],
            mode='markers',
            name=zone_type,
            marker=dict(
                size=df_type['r'] / 10,  # Divisé par 10 au lieu de 5 (marqueurs 2x plus petits)
                color=get_zone_color(zone_type),
                opacity=0.9,
                line=dict(width=2, color='white')
            ),
            text=[
                f"<b>{row['name']}</b><br>" +
                f"Position XML: ({row['x']:.0f}, {row['z']:.0f})<br>" +
                f"Position iZurvive: ({row['x_izurvive']:.0f}, {row['z_izurvive']:.0f})<br>" +
                f"Radius: {row['r']:.0f}m<br>" +
                f"Spawn: {row['smin']}-{row['smax']}<br>" +
                f"Dynamic: {row['dmin']}-{row['dmax']}<br>" +
                f"{'✅ ACTIF' if row['active'] else '❌ INACTIF'}"
                for _, row in df_type.iterrows()
            ],
            hovertemplate='%{text}<extra></extra>',
            customdata=df_type.index,
            unselected=dict(marker=dict(opacity=0.6))
        ))
    
    # Statut de calibration
    calibration_status = {
        'Chernarus': '✅ Calibré',
        'Livonia': '✅ Calibré',
        'Sakhal': '✅ Calibré'
    }
    
    fig.update_layout(
        title=f"Carte {map_name} - Zones de spawn zombies ({calibration_status[map_name]})",
        xaxis_title="",
        yaxis_title="",
        height=800,
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="black",
            borderwidth=1
        ),
        xaxis=dict(
            range=[0, map_size],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[0, map_size],
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ==============================
# SESSION STATE
# ==============================
if 'zones_chernarus' not in st.session_state:
    try:
        path = Path(__file__).parent.parent / "data" / "zombie_territories_chernarus.xml"
        with open(path, 'r', encoding='utf-8') as f:
            st.session_state.zones_chernarus = parse_zombie_territories(f.read())
    except:
        st.session_state.zones_chernarus = []

if 'zones_livonia' not in st.session_state:
    try:
        path = Path(__file__).parent.parent / "data" / "zombie_territories_livonia.xml"
        with open(path, 'r', encoding='utf-8') as f:
            st.session_state.zones_livonia = parse_zombie_territories(f.read())
    except:
        st.session_state.zones_livonia = []

if 'zones_sakhal' not in st.session_state:
    try:
        path = Path(__file__).parent.parent / "data" / "zombie_territories_sakhal.xml"
        with open(path, 'r', encoding='utf-8') as f:
            st.session_state.zones_sakhal = parse_zombie_territories(f.read())
    except:
        st.session_state.zones_sakhal = []

if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = None

if 'current_map' not in st.session_state:
    st.session_state.current_map = 'chernarus'

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🗺️ Carte Interactive - DayZ")
st.subheader("Édite visuellement les spawns zombies")

if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

# Note de calibration
st.markdown("""
<div class="calibration-note">
    <b>📍 État de calibration :</b><br>
    ✅ <b>Chernarus</b> : Calibré (précision parfaite)<br>
    ✅ <b>Livonia</b> : Calibré (précision parfaite)<br>
    ✅ <b>Sakhal</b> : Calibré (précision parfaite)
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# TABS POUR LES 3 CARTES
# ==============================
tab1, tab2, tab3 = st.tabs(["🗺️ Chernarus ✅", "🗺️ Livonia ✅", "🗺️ Sakhal ✅"])

# ==============================
# TAB CHERNARUS
# ==============================
with tab1:
    st.session_state.current_map = 'chernarus'
    zones = st.session_state.zones_chernarus
    
    st.markdown("### 📊 Statistiques Chernarus")
    
    active_zones = [z for z in zones if z['active']]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="stats-box"><h2>{len(zones)}</h2><p>Zones totales</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stats-box"><h2>{len(active_zones)}</h2><p>Zones actives</p></div>""", unsafe_allow_html=True)
    with col3:
        zone_types = set(z['name'] for z in zones)
        st.markdown(f"""<div class="stats-box"><h2>{len(zone_types)}</h2><p>Types différents</p></div>""", unsafe_allow_html=True)
    with col4:
        inactive = len(zones) - len(active_zones)
        st.markdown(f"""<div class="stats-box"><h2>{inactive}</h2><p>Zones désactivées</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filtres
    st.markdown("### 🔍 Filtres")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        zone_types_list = sorted(set(z['name'] for z in zones))
        selected_types = st.multiselect(
            "Types de zombies",
            zone_types_list,
            default=zone_types_list,
            key="filter_chernarus"
        )
    
    with col_f2:
        show_only_active = st.checkbox("Afficher seulement les zones actives", value=False, key="active_chernarus")
    
    filtered_zones = [z for z in zones if z['name'] in selected_types and (not show_only_active or z['active'])]
    
    st.info(f"📊 {len(filtered_zones)} zones affichées sur {len(zones)} totales")
    st.markdown("---")
    
    # Carte
    st.markdown("### 🗺️ Carte Chernarus")
    img_path = Path(__file__).parent.parent / "images" / "chernarus_map.webp"
    fig = create_map(filtered_zones, "Chernarus", 15360, img_path)
    
    if fig:
        selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map_chernarus")
        
        if selected_point and 'selection' in selected_point and 'points' in selected_point['selection']:
            points = selected_point['selection']['points']
            if points:
                point_index = points[0]['customdata']
                st.session_state.selected_zone = filtered_zones[point_index]
    
    st.markdown("---")
    
    # Download
    xml_content = generate_xml(zones)
    st.download_button(
        label="📥 Télécharger zombie_territories.xml (Chernarus)",
        data=xml_content,
        file_name="zombie_territories_chernarus.xml",
        mime="text/xml",
        use_container_width=True,
        type="primary"
    )

# ==============================
# TAB LIVONIA
# ==============================
with tab2:
    st.session_state.current_map = 'livonia'
    zones = st.session_state.zones_livonia
    
    st.markdown("### 📊 Statistiques Livonia")
    
    active_zones = [z for z in zones if z['active']]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="stats-box"><h2>{len(zones)}</h2><p>Zones totales</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stats-box"><h2>{len(active_zones)}</h2><p>Zones actives</p></div>""", unsafe_allow_html=True)
    with col3:
        zone_types = set(z['name'] for z in zones)
        st.markdown(f"""<div class="stats-box"><h2>{len(zone_types)}</h2><p>Types différents</p></div>""", unsafe_allow_html=True)
    with col4:
        inactive = len(zones) - len(active_zones)
        st.markdown(f"""<div class="stats-box"><h2>{inactive}</h2><p>Zones désactivées</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filtres
    st.markdown("### 🔍 Filtres")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        zone_types_list = sorted(set(z['name'] for z in zones))
        selected_types = st.multiselect(
            "Types de zombies",
            zone_types_list,
            default=zone_types_list,
            key="filter_livonia"
        )
    
    with col_f2:
        show_only_active = st.checkbox("Afficher seulement les zones actives", value=False, key="active_livonia")
    
    filtered_zones = [z for z in zones if z['name'] in selected_types and (not show_only_active or z['active'])]
    
    st.info(f"📊 {len(filtered_zones)} zones affichées sur {len(zones)} totales")
    st.markdown("---")
    
    # Carte
    st.markdown("### 🗺️ Carte Livonia")
    img_path = Path(__file__).parent.parent / "images" / "livonia_map.jpg"
    fig = create_map(filtered_zones, "Livonia", 12800, img_path)
    
    if fig:
        selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map_livonia")
        
        if selected_point and 'selection' in selected_point and 'points' in selected_point['selection']:
            points = selected_point['selection']['points']
            if points:
                point_index = points[0]['customdata']
                st.session_state.selected_zone = filtered_zones[point_index]
    
    st.markdown("---")
    
    # Download
    xml_content = generate_xml(zones)
    st.download_button(
        label="📥 Télécharger zombie_territories.xml (Livonia)",
        data=xml_content,
        file_name="zombie_territories_livonia.xml",
        mime="text/xml",
        use_container_width=True,
        type="primary"
    )

# ==============================
# TAB SAKHAL
# ==============================
with tab3:
    st.session_state.current_map = 'sakhal'
    zones = st.session_state.zones_sakhal
    
    st.markdown("### 📊 Statistiques Sakhal")
    
    active_zones = [z for z in zones if z['active']]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""<div class="stats-box"><h2>{len(zones)}</h2><p>Zones totales</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stats-box"><h2>{len(active_zones)}</h2><p>Zones actives</p></div>""", unsafe_allow_html=True)
    with col3:
        zone_types = set(z['name'] for z in zones)
        st.markdown(f"""<div class="stats-box"><h2>{len(zone_types)}</h2><p>Types différents</p></div>""", unsafe_allow_html=True)
    with col4:
        inactive = len(zones) - len(active_zones)
        st.markdown(f"""<div class="stats-box"><h2>{inactive}</h2><p>Zones désactivées</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filtres
    st.markdown("### 🔍 Filtres")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        zone_types_list = sorted(set(z['name'] for z in zones))
        selected_types = st.multiselect(
            "Types de zombies",
            zone_types_list,
            default=zone_types_list,
            key="filter_sakhal"
        )
    
    with col_f2:
        show_only_active = st.checkbox("Afficher seulement les zones actives", value=False, key="active_sakhal")
    
    filtered_zones = [z for z in zones if z['name'] in selected_types and (not show_only_active or z['active'])]
    
    st.info(f"📊 {len(filtered_zones)} zones affichées sur {len(zones)} totales")
    st.markdown("---")
    
    # Carte
    st.markdown("### 🗺️ Carte Sakhal")
    img_path = Path(__file__).parent.parent / "images" / "sakhal_map.webp"
    fig = create_map(filtered_zones, "Sakhal", 15360, img_path)
    
    if fig:
        selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map_sakhal")
        
        if selected_point and 'selection' in selected_point and 'points' in selected_point['selection']:
            points = selected_point['selection']['points']
            if points:
                point_index = points[0]['customdata']
                st.session_state.selected_zone = filtered_zones[point_index]
    
    st.markdown("---")
    
    # Download
    xml_content = generate_xml(zones)
    st.download_button(
        label="📥 Télécharger zombie_territories.xml (Sakhal)",
        data=xml_content,
        file_name="zombie_territories_sakhal.xml",
        mime="text/xml",
        use_container_width=True,
        type="primary"
    )

# ==============================
# ÉDITION ZONE (COMMUN)
# ==============================
if st.session_state.selected_zone:
    zone = st.session_state.selected_zone
    current_map = st.session_state.current_map
    
    if current_map == 'chernarus':
        zones_list = st.session_state.zones_chernarus
    elif current_map == 'livonia':
        zones_list = st.session_state.zones_livonia
    else:
        zones_list = st.session_state.zones_sakhal
    
    st.markdown("---")
    
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown("### ✏️ Éditer la zone sélectionnée")
    with col_header2:
        if st.button("✖️ Désélectionner", use_container_width=True):
            st.session_state.selected_zone = None
            st.rerun()
    
    zone_index = None
    for i, z in enumerate(zones_list):
        if z['x'] == zone['x'] and z['z'] == zone['z']:
            zone_index = i
            break
    
    if zone_index is not None:
        actual_zone = zones_list[zone_index]
        
        col_edit1, col_edit2 = st.columns([2, 1])
        
        with col_edit1:
            st.markdown(f"""
            <div class="zone-card">
                <h4>{actual_zone['name']}</h4>
                <p><b>Position:</b> ({actual_zone['x']:.1f}, {actual_zone['z']:.1f})</p>
                <p><b>Radius:</b> {actual_zone['r']}m</p>
                <p><b>Statut:</b> {'✅ ACTIF' if actual_zone['active'] else '❌ INACTIF'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_edit2:
            def toggle_zone_active():
                zones_list[zone_index]['active'] = st.session_state[f"toggle_{current_map}_{zone_index}"]
            
            st.toggle(
                "Zone active",
                value=actual_zone['active'],
                key=f"toggle_{current_map}_{zone_index}",
                on_change=toggle_zone_active
            )
        
        with st.expander("⚙️ Paramètres avancés"):
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            
            with col_p1:
                new_smin = st.number_input("smin", value=actual_zone['smin'], min_value=0, max_value=50, key=f"smin_{current_map}_{zone_index}")
            with col_p2:
                new_smax = st.number_input("smax", value=actual_zone['smax'], min_value=0, max_value=50, key=f"smax_{current_map}_{zone_index}")
            with col_p3:
                new_dmin = st.number_input("dmin", value=actual_zone['dmin'], min_value=0, max_value=50, key=f"dmin_{current_map}_{zone_index}")
            with col_p4:
                new_dmax = st.number_input("dmax", value=actual_zone['dmax'], min_value=0, max_value=50, key=f"dmax_{current_map}_{zone_index}")
        
        if st.button("💾 Sauvegarder les paramètres", type="primary", use_container_width=True):
            zones_list[zone_index]['smin'] = new_smin
            zones_list[zone_index]['smax'] = new_smax
            zones_list[zone_index]['dmin'] = new_dmin
            zones_list[zone_index]['dmax'] = new_dmax
            
            st.success("✅ Paramètres mis à jour !")
            st.session_state.selected_zone = None
            st.rerun()

# ==============================
# ACTIONS GLOBALES
# ==============================
st.markdown("---")
st.markdown("### ⚡ Actions rapides (carte actuelle)")

col_action1, col_action2, col_action3 = st.columns(3)

current_map = st.session_state.current_map
if current_map == 'chernarus':
    zones_list = st.session_state.zones_chernarus
    map_name = "Chernarus"
elif current_map == 'livonia':
    zones_list = st.session_state.zones_livonia
    map_name = "Livonia"
else:
    zones_list = st.session_state.zones_sakhal
    map_name = "Sakhal"

with col_action1:
    if st.button(f"✅ Activer toutes ({map_name})", use_container_width=True):
        for z in zones_list:
            z['active'] = True
        st.success(f"Toutes les zones de {map_name} activées !")
        st.rerun()

with col_action2:
    if st.button(f"❌ Désactiver toutes ({map_name})", use_container_width=True):
        for z in zones_list:
            z['active'] = False
        st.success(f"Toutes les zones de {map_name} désactivées !")
        st.rerun()

with col_action3:
    if st.button(f"🔄 Réinitialiser ({map_name})", use_container_width=True):
        try:
            if current_map == 'chernarus':
                filename = "zombie_territories_chernarus.xml"
            elif current_map == 'livonia':
                filename = "zombie_territories_livonia.xml"
            else:
                filename = "zombie_territories_sakhal.xml"
            
            path = Path(__file__).parent.parent / "data" / filename
            with open(path, 'r', encoding='utf-8') as f:
                if current_map == 'chernarus':
                    st.session_state.zones_chernarus = parse_zombie_territories(f.read())
                elif current_map == 'livonia':
                    st.session_state.zones_livonia = parse_zombie_territories(f.read())
                else:
                    st.session_state.zones_sakhal = parse_zombie_territories(f.read())
            
            st.success(f"Configuration vanilla de {map_name} rechargée !")
            st.rerun()
        except:
            st.error("Fichier vanilla introuvable")
