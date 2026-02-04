"""
Codex Suite - Carte Interactive Chernarus
Éditeur visuel des spawns zombies - Style iZurvive
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
    page_title="Codex - Carte Chernarus",
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
                'active': True  # Par défaut activé
            })
    
    return zones

def get_zone_color(zone_name):
    """Retourne une couleur selon le type de zombie"""
    color_map = {
        'InfectedArmy': '#8B0000',           # Rouge foncé
        'InfectedArmyHard': '#DC143C',       # Rouge vif
        'InfectedCity': '#4169E1',           # Bleu
        'InfectedIndustrial': '#FF8C00',     # Orange
        'InfectedVillage': '#32CD32',        # Vert
        'InfectedPolice': '#191970',         # Bleu marine
        'InfectedMedic': '#FF1493',          # Rose
        'InfectedPrisoner': '#8B4513',       # Marron
        'InfectedFirefighter': '#FF4500',    # Orange rouge
        'InfectedReligious': '#9370DB',      # Violet
    }
    
    for key, color in color_map.items():
        if key in zone_name:
            return color
    
    return '#808080'  # Gris par défaut

def generate_xml(zones):
    """Génère le XML depuis la liste de zones"""
    # Grouper par couleur (territory)
    territories = {}
    for zone in zones:
        if zone['active']:  # Seulement les zones actives
            color = zone['color']
            if color not in territories:
                territories[color] = []
            territories[color].append(zone)
    
    # Construire le XML
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<territory-type>')
    
    for color, zones_list in territories.items():
        xml_lines.append(f'    <territory color="{color}">')
        for zone in zones_list:
            xml_lines.append(
                f'        <zone name="{zone["name"]}" '
                f'smin="{zone["smin"]}" smax="{zone["smax"]}" '
                f'dmin="{zone["dmin"]}" dmax="{zone["dmax"]}" '
                f'x="{zone["x"]}" z="{zone["z"]}" r="{zone["r"]}"/>'
            )
        xml_lines.append('    </territory>')
    
    xml_lines.append('</territory-type>')
    
    return '\n'.join(xml_lines)

# ==============================
# SESSION STATE
# ==============================
if 'zones' not in st.session_state:
    # Charger le fichier vanilla par défaut
    try:
        vanilla_path = Path(__file__).parent.parent / "data" / "zombie_territories_chernarus.xml"
        with open(vanilla_path, 'r', encoding='utf-8') as f:
            st.session_state.zones = parse_zombie_territories(f.read())
    except:
        st.session_state.zones = []

if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = None

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🗺️ Carte Interactive - Chernarus")
st.subheader("Édite visuellement les spawns zombies")

if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

st.markdown("---")

# ==============================
# UPLOAD FICHIER
# ==============================
st.markdown("### 📤 Charger ton fichier")

uploaded = st.file_uploader(
    "Charge ton zombie_territories.xml (optionnel)",
    type=["xml"],
    help="Si tu ne charges rien, le fichier vanilla sera utilisé"
)

if uploaded:
    content = uploaded.read().decode("utf-8")
    st.session_state.zones = parse_zombie_territories(content)
    st.success(f"✅ {len(st.session_state.zones)} zones chargées !")

st.markdown("---")

# ==============================
# STATISTIQUES
# ==============================
zones = st.session_state.zones
active_zones = [z for z in zones if z['active']]

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown(f"""
    <div class="stats-box">
        <h2>{len(zones)}</h2>
        <p>Zones totales</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div class="stats-box">
        <h2>{len(active_zones)}</h2>
        <p>Zones actives</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    zone_types = set(z['name'] for z in zones)
    st.markdown(f"""
    <div class="stats-box">
        <h2>{len(zone_types)}</h2>
        <p>Types différents</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    inactive_zones = len(zones) - len(active_zones)
    st.markdown(f"""
    <div class="stats-box">
        <h2>{inactive_zones}</h2>
        <p>Zones désactivées</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================
# FILTRES
# ==============================
st.markdown("### 🔍 Filtres")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    zone_types_list = sorted(set(z['name'] for z in zones))
    selected_types = st.multiselect(
        "Types de zombies",
        zone_types_list,
        default=zone_types_list,
        help="Sélectionne les types à afficher sur la carte"
    )

with col_filter2:
    show_only_active = st.checkbox("Afficher seulement les zones actives", value=False)

# Filtrer les zones
filtered_zones = [
    z for z in zones 
    if z['name'] in selected_types and (not show_only_active or z['active'])
]

st.info(f"📊 {len(filtered_zones)} zones affichées sur {len(zones)} totales")

st.markdown("---")

# ==============================
# CARTE INTERACTIVE
# ==============================
st.markdown("### 🗺️ Carte Chernarus")

# Préparer les données pour Plotly
df = pd.DataFrame(filtered_zones)

if len(df) > 0:
    # Créer la figure Plotly avec image de fond
    fig = go.Figure()
    
    # Charger et ajouter l'image de fond
    from PIL import Image
    import base64
    from io import BytesIO
    
    try:
        # Charger l'image de Chernarus
        img_path = Path(__file__).parent.parent / "images" / "chernarus_map.webp"
        img = Image.open(img_path)
        
        # Convertir en base64 pour Plotly
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Ajouter l'image comme fond
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_str}",
                xref="x",
                yref="y",
                x=0,
                y=15360,
                sizex=15360,
                sizey=15360,
                sizing="stretch",
                opacity=0.7,
                layer="below"
            )
        )
    except Exception as e:
        # Si l'image n'est pas trouvée, on continue sans fond
        st.warning(f"⚠️ Image de fond non trouvée. Assure-toi que `chernarus_map.webp` est dans `images/`")
    
    # Ajouter les marqueurs par type
    for zone_type in df['name'].unique():
        df_type = df[df['name'] == zone_type]
        
        fig.add_trace(go.Scatter(
            x=df_type['x'],
            y=15360 - df_type['z'],  # Inverser Z pour correspondre à l'image
            mode='markers',
            name=zone_type,
            marker=dict(
                size=df_type['r'] / 5,  # Taille proportionnelle au radius
                color=get_zone_color(zone_type),
                opacity=0.9,  # ← Augmenté de 0.8 à 0.9 pour meilleure visibilité
                line=dict(width=2, color='white')
            ),
            text=[
                f"<b>{row['name']}</b><br>" +
                f"Position: ({row['x']:.0f}, {row['z']:.0f})<br>" +
                f"Radius: {row['r']:.0f}m<br>" +
                f"Spawn: {row['smin']}-{row['smax']}<br>" +
                f"Dynamic: {row['dmin']}-{row['dmax']}<br>" +
                f"{'✅ ACTIF' if row['active'] else '❌ INACTIF'}"
                for _, row in df_type.iterrows()
            ],
            hovertemplate='%{text}<extra></extra>',
            customdata=df_type.index,
            unselected=dict(marker=dict(opacity=0.6))  # ← Opacité des points NON sélectionnés
        ))
    
    # Mise en forme de la carte
    fig.update_layout(
        title="Carte Chernarus - Zones de spawn zombies (style iZurvive)",
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
            range=[0, 15360],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[0, 15360],
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Afficher la carte
    selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="map")
    
    # Gestion du clic
    if selected_point and 'selection' in selected_point and 'points' in selected_point['selection']:
        points = selected_point['selection']['points']
        if points:
            point_index = points[0]['customdata']
            st.session_state.selected_zone = filtered_zones[point_index]

else:
    st.warning("Aucune zone à afficher avec les filtres actuels")

st.markdown("---")

# ==============================
# ÉDITION ZONE SÉLECTIONNÉE
# ==============================
if st.session_state.selected_zone:
    zone = st.session_state.selected_zone
    
    # Bouton désélection en haut
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown("### ✏️ Éditer la zone sélectionnée")
    with col_header2:
        if st.button("✖️ Désélectionner", use_container_width=True):
            st.session_state.selected_zone = None
            st.rerun()
    
    col_edit1, col_edit2 = st.columns([2, 1])
    
    # Trouver l'index de la zone dans la liste
    zone_index = None
    for i, z in enumerate(st.session_state.zones):
        if z['x'] == zone['x'] and z['z'] == zone['z']:
            zone_index = i
            break
    
    if zone_index is not None:
        actual_zone = st.session_state.zones[zone_index]
        
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
            # Toggle avec callback pour mettre à jour directement
            def toggle_zone_active():
                st.session_state.zones[zone_index]['active'] = st.session_state[f"toggle_{zone_index}"]
            
            st.toggle(
                "Zone active",
                value=actual_zone['active'],
                key=f"toggle_{zone_index}",
                on_change=toggle_zone_active
            )
        
        # Paramètres avancés
        with st.expander("⚙️ Paramètres avancés"):
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            
            with col_p1:
                new_smin = st.number_input("smin", value=actual_zone['smin'], min_value=0, max_value=50, key=f"smin_{zone_index}")
            with col_p2:
                new_smax = st.number_input("smax", value=actual_zone['smax'], min_value=0, max_value=50, key=f"smax_{zone_index}")
            with col_p3:
                new_dmin = st.number_input("dmin", value=actual_zone['dmin'], min_value=0, max_value=50, key=f"dmin_{zone_index}")
            with col_p4:
                new_dmax = st.number_input("dmax", value=actual_zone['dmax'], min_value=0, max_value=50, key=f"dmax_{zone_index}")
        
        # Bouton pour sauvegarder les paramètres avancés
        if st.button("💾 Sauvegarder les paramètres", type="primary", use_container_width=True):
            st.session_state.zones[zone_index]['smin'] = new_smin
            st.session_state.zones[zone_index]['smax'] = new_smax
            st.session_state.zones[zone_index]['dmin'] = new_dmin
            st.session_state.zones[zone_index]['dmax'] = new_dmax
            
            st.success("✅ Paramètres mis à jour !")
            st.session_state.selected_zone = None
            st.rerun()

st.markdown("---")

# ==============================
# ACTIONS GLOBALES
# ==============================
st.markdown("### ⚡ Actions rapides")

col_action1, col_action2, col_action3 = st.columns(3)

with col_action1:
    if st.button("✅ Activer toutes les zones", use_container_width=True):
        for z in st.session_state.zones:
            z['active'] = True
        st.success("Toutes les zones activées !")
        st.rerun()

with col_action2:
    if st.button("❌ Désactiver toutes les zones", use_container_width=True):
        for z in st.session_state.zones:
            z['active'] = False
        st.success("Toutes les zones désactivées !")
        st.rerun()

with col_action3:
    if st.button("🔄 Réinitialiser (vanilla)", use_container_width=True):
        try:
            vanilla_path = Path(__file__).parent.parent / "data" / "zombie_territories_chernarus.xml"
            with open(vanilla_path, 'r', encoding='utf-8') as f:
                st.session_state.zones = parse_zombie_territories(f.read())
            st.success("Configuration vanilla rechargée !")
            st.rerun()
        except:
            st.error("Fichier vanilla introuvable")

st.markdown("---")

# ==============================
# GÉNÉRATION ET TÉLÉCHARGEMENT
# ==============================
st.markdown("### 💾 Télécharger le fichier modifié")

xml_content = generate_xml(st.session_state.zones)

st.download_button(
    label="📥 Télécharger zombie_territories.xml",
    data=xml_content,
    file_name="zombie_territories.xml",
    mime="text/xml",
    use_container_width=True,
    type="primary"
)

# Aperçu
with st.expander("👀 Aperçu du XML généré"):
    st.code(xml_content[:2000] + "\n...\n(fichier tronqué)", language="xml")

st.info(f"📊 Le fichier contient {len(active_zones)} zones actives sur {len(zones)} totales")
