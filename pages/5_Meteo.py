"""
CodeX Suite — Configurateur Météo
Génère un cfgweather.xml personnalisé avec prévisualisation visuelle
"""

import streamlit as st
import sys
from pathlib import Path
import math
import plotly.graph_objects as go

st.set_page_config(
    page_title="CodeX — Météo",
    page_icon="images/favicon.png",
    layout="wide",
)

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import apply_styles, apply_header
apply_styles(st)
apply_header(st)

# ─────────────────────────────────────────────
#  STYLE SPÉCIFIQUE MÉTÉO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Preset buttons */
    .preset-grid { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1.5rem; }
    .preset-btn {
        flex: 1;
        min-width: 120px;
        background: rgba(0, 25, 50, 0.7);
        border: 1px solid rgba(0, 212, 255, 0.25);
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.25s ease;
        color: rgba(255,255,255,0.85);
    }
    .preset-btn:hover {
        border-color: #00D4FF;
        background: rgba(0, 212, 255, 0.12);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.2);
    }
    .preset-icon { font-size: 28px; display: block; margin-bottom: 6px; }
    .preset-name { font-size: 13px; font-weight: 700; color: #00D4FF; }

    /* Section météo */
    .weather-section {
        background: rgba(0, 25, 50, 0.55);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .weather-section-title {
        font-size: 15px;
        font-weight: 700;
        color: #00D4FF;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Info badge */
    .info-badge {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 12px;
        color: rgba(255,255,255,0.7);
        margin-top: 4px;
    }

    /* XML preview */
    .xml-preview {
        background: #0a0f1a;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        line-height: 1.7;
        color: #a8d8ea;
        max-height: 500px;
        overflow-y: auto;
    }
    .xml-tag    { color: #00D4FF; }
    .xml-attr   { color: #ffd700; }
    .xml-val    { color: #00FF88; }
    .xml-comment{ color: #546e7a; font-style: italic; }

    /* Toggle switches */
    .toggle-row {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 12px;
    }

    /* Slider labels custom */
    .slider-label {
        font-size: 12px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 2px;
    }
    .slider-value {
        font-size: 18px;
        font-weight: 800;
        color: #00D4FF;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────
if st.button("← Accueil", key="home"):
    st.switch_page("app.py")

st.markdown("## 🌦️ Configurateur Météo")
st.markdown('<p style="color:rgba(255,255,255,0.5);margin-top:-10px;">Génère ton cfgweather.xml personnalisé avec prévisualisation en temps réel</p>', unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
#  PRÉSETS
# ─────────────────────────────────────────────
PRESETS = {
    "Ensoleillé": {
        "icon": "☀️",
        "overcast_cur": 0.1, "overcast_min": 0.0, "overcast_max": 0.3,
        "fog_cur": 0.0, "fog_min": 0.0, "fog_max": 0.05,
        "rain_cur": 0.0, "rain_min": 0.0, "rain_max": 0.0,
        "wind_cur": 4.0, "wind_min": 1.0, "wind_max": 8.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 0.0, "storm_threshold": 0.98, "storm_timeout": 120,
    },
    "Nuageux": {
        "icon": "⛅",
        "overcast_cur": 0.6, "overcast_min": 0.4, "overcast_max": 0.9,
        "fog_cur": 0.05, "fog_min": 0.0, "fog_max": 0.15,
        "rain_cur": 0.1, "rain_min": 0.0, "rain_max": 0.3,
        "wind_cur": 8.0, "wind_min": 3.0, "wind_max": 12.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 0.3, "storm_threshold": 0.9, "storm_timeout": 90,
    },
    "Brouillard": {
        "icon": "🌫️",
        "overcast_cur": 0.6, "overcast_min": 0.4, "overcast_max": 0.8,
        "fog_cur": 0.7, "fog_min": 0.5, "fog_max": 1.0,
        "rain_cur": 0.0, "rain_min": 0.0, "rain_max": 0.1,
        "wind_cur": 2.0, "wind_min": 0.0, "wind_max": 5.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 0.0, "storm_threshold": 0.98, "storm_timeout": 120,
    },
    "Pluvieux": {
        "icon": "🌧️",
        "overcast_cur": 0.85, "overcast_min": 0.6, "overcast_max": 1.0,
        "fog_cur": 0.1, "fog_min": 0.05, "fog_max": 0.4,
        "rain_cur": 0.6, "rain_min": 0.3, "rain_max": 0.9,
        "wind_cur": 10.0, "wind_min": 5.0, "wind_max": 15.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 0.5, "storm_threshold": 0.85, "storm_timeout": 60,
    },
    "Tempête": {
        "icon": "⛈️",
        "overcast_cur": 0.95, "overcast_min": 0.8, "overcast_max": 1.0,
        "fog_cur": 0.2, "fog_min": 0.1, "fog_max": 0.5,
        "rain_cur": 0.9, "rain_min": 0.7, "rain_max": 1.0,
        "wind_cur": 18.0, "wind_min": 12.0, "wind_max": 20.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 1.0, "storm_threshold": 0.85, "storm_timeout": 30,
    },
    "Neige (Sakhal)": {
        "icon": "❄️",
        "overcast_cur": 0.7, "overcast_min": 0.3, "overcast_max": 1.0,
        "fog_cur": 0.1, "fog_min": 0.0, "fog_max": 0.3,
        "rain_cur": 0.0, "rain_min": 0.0, "rain_max": 0.0,
        "wind_cur": 8.0, "wind_min": 2.0, "wind_max": 15.0,
        "snow_cur": 0.6, "snow_min": 0.0, "snow_max": 1.0,
        "storm_density": 0.3, "storm_threshold": 0.98, "storm_timeout": 90,
    },
    "Dynamique": {
        "icon": "🎲",
        "overcast_cur": 0.45, "overcast_min": 0.07, "overcast_max": 1.0,
        "fog_cur": 0.05, "fog_min": 0.0, "fog_max": 0.5,
        "rain_cur": 0.0, "rain_min": 0.0, "rain_max": 1.0,
        "wind_cur": 8.0, "wind_min": 0.0, "wind_max": 20.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 1.0, "storm_threshold": 0.9, "storm_timeout": 45,
    },
    "Vanilla": {
        "icon": "🎮",
        "overcast_cur": 0.45, "overcast_min": 0.07, "overcast_max": 1.0,
        "fog_cur": 0.0, "fog_min": 0.0, "fog_max": 0.0,
        "rain_cur": 0.0, "rain_min": 0.0, "rain_max": 0.0,
        "wind_cur": 8.0, "wind_min": 0.0, "wind_max": 20.0,
        "snow_cur": 0.0, "snow_min": 0.0, "snow_max": 0.0,
        "storm_density": 1.0, "storm_threshold": 0.98, "storm_timeout": 45,
    },
}

# Initialisation session_state avec Vanilla par défaut
if "preset_loaded" not in st.session_state:
    for k, v in PRESETS["Vanilla"].items():
        if k != "icon":
            st.session_state[f"w_{k}"] = v
    st.session_state.preset_loaded = True
    st.session_state.active_preset = "Vanilla"

# Boutons présets
st.markdown("### 🎨 Présets rapides")
cols = st.columns(len(PRESETS))
for i, (name, data) in enumerate(PRESETS.items()):
    with cols[i]:
        if st.button(f"{data['icon']}\n{name}", key=f"preset_{name}", use_container_width=True):
            for k, v in data.items():
                if k != "icon":
                    st.session_state[f"w_{k}"] = v
                    st.session_state[f"s_{k}"] = v  # force le slider
            st.session_state.active_preset = name
            st.rerun()

# Indicateur préset actif
st.markdown(f'<div class="info-badge">📌 Préset actif : <strong>{st.session_state.get("active_preset","Personnalisé")}</strong> — modifie les sliders pour personnaliser</div>', unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
#  CONFIGURATION DÉTAILLÉE
# ─────────────────────────────────────────────
st.markdown("### ⚙️ Configuration détaillée")

col_left, col_right = st.columns(2, gap="large")

# ── COLONNE GAUCHE ────────────────────────────
with col_left:

    # Options globales
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">🔧 Options globales</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        enable = st.toggle("Activer le fichier", value=True, help="enable=1 : le fichier cfgweather.xml est pris en compte")
    with c2:
        reset = st.toggle("Reset au restart", value=False, help="reset=0 : conserve la météo entre les restarts")
    st.markdown('</div>', unsafe_allow_html=True)

    # Overcast
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">☁️ Overcast — Couverture nuageuse</div>', unsafe_allow_html=True)
    st.caption("Valeur actuelle (point de départ)")
    overcast_cur = st.slider("Overcast actuel", 0.0, 1.0, float(st.session_state.get("w_overcast_cur", 0.45)), 0.01, key="s_overcast_cur", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Min possible")
        overcast_min = st.slider("Overcast min", 0.0, 1.0, float(st.session_state.get("w_overcast_min", 0.07)), 0.01, key="s_overcast_min", label_visibility="collapsed")
    with c2:
        st.caption("Max possible")
        overcast_max = st.slider("Overcast max", 0.0, 1.0, float(st.session_state.get("w_overcast_max", 1.0)), 0.01, key="s_overcast_max", label_visibility="collapsed")
    st.markdown(f'<div class="info-badge">Actuel: <strong>{overcast_cur:.2f}</strong> | Plage: {overcast_min:.2f} → {overcast_max:.2f} {"☀️ Ciel dégagé" if overcast_cur < 0.3 else "⛅ Partiellement nuageux" if overcast_cur < 0.7 else "☁️ Très nuageux"}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fog
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">🌫️ Brouillard</div>', unsafe_allow_html=True)
    fog_cur = st.slider("Brouillard actuel", 0.0, 1.0, float(st.session_state.get("w_fog_cur", 0.0)), 0.01, key="s_fog_cur", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Min possible")
        fog_min = st.slider("Fog min", 0.0, 1.0, float(st.session_state.get("w_fog_min", 0.0)), 0.01, key="s_fog_min", label_visibility="collapsed")
    with c2:
        st.caption("Max possible")
        fog_max = st.slider("Fog max", 0.0, 1.0, float(st.session_state.get("w_fog_max", 0.0)), 0.01, key="s_fog_max", label_visibility="collapsed")
    st.markdown(f'<div class="info-badge">Actuel: <strong>{fog_cur:.2f}</strong> | {"🟢 Aucun brouillard" if fog_cur < 0.1 else "🟡 Brouillard modéré" if fog_cur < 0.5 else "🔴 Brouillard dense — impact visibilité fort"}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Rain
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">🌧️ Pluie</div>', unsafe_allow_html=True)
    rain_cur = st.slider("Pluie actuelle", 0.0, 1.0, float(st.session_state.get("w_rain_cur", 0.0)), 0.01, key="s_rain_cur", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Min possible")
        rain_min = st.slider("Rain min", 0.0, 1.0, float(st.session_state.get("w_rain_min", 0.0)), 0.01, key="s_rain_min", label_visibility="collapsed")
    with c2:
        st.caption("Max possible")
        rain_max = st.slider("Rain max", 0.0, 1.0, float(st.session_state.get("w_rain_max", 0.0)), 0.01, key="s_rain_max", label_visibility="collapsed")
    st.caption("Seuil overcast pour déclencher la pluie")
    c1, c2 = st.columns(2)
    with c1:
        rain_thresh_min = st.slider("Seuil overcast min", 0.0, 1.0, 0.6, 0.01, key="s_rain_thresh_min", label_visibility="collapsed")
    with c2:
        rain_thresh_max = st.slider("Seuil overcast max", 0.0, 1.0, 1.0, 0.01, key="s_rain_thresh_max", label_visibility="collapsed")
    if rain_max > 0 and overcast_max < rain_thresh_min:
        st.warning("⚠️ Overcast max insuffisant pour déclencher la pluie !")
    st.markdown('</div>', unsafe_allow_html=True)

# ── COLONNE DROITE ────────────────────────────
with col_right:

    # Vent
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">💨 Vent</div>', unsafe_allow_html=True)
    st.caption("Vitesse actuelle (m/s)")
    wind_cur = st.slider("Vent actuel", 0.0, 20.0, float(st.session_state.get("w_wind_cur", 8.0)), 0.5, key="s_wind_cur", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Min (m/s)")
        wind_min = st.slider("Vent min", 0.0, 20.0, float(st.session_state.get("w_wind_min", 0.0)), 0.5, key="s_wind_min", label_visibility="collapsed")
    with c2:
        st.caption("Max (m/s)")
        wind_max = st.slider("Vent max", 0.0, 20.0, float(st.session_state.get("w_wind_max", 20.0)), 0.5, key="s_wind_max", label_visibility="collapsed")
    st.caption("Direction (radians)")
    wind_dir = st.slider("Direction", -3.14, 3.14, 0.0, 0.1, key="s_wind_dir", label_visibility="collapsed")
    dir_label = "Nord ↑" if abs(wind_dir) < 0.3 else "Est →" if 1.2 < wind_dir < 2.0 else "Ouest ←" if -2.0 < wind_dir < -1.2 else "Sud ↓" if abs(abs(wind_dir) - 3.14) < 0.3 else f"{wind_dir:.2f} rad"
    st.markdown(f'<div class="info-badge">Vitesse: <strong>{wind_cur:.1f} m/s</strong> | Direction: {dir_label} | {"🍃 Brise légère" if wind_cur < 6 else "💨 Vent modéré" if wind_cur < 12 else "🌪️ Vent fort"}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Neige
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">❄️ Neige <span style="font-size:11px;color:rgba(255,255,255,0.4);font-weight:400;">(Sakhal uniquement)</span></div>', unsafe_allow_html=True)
    snow_cur = st.slider("Neige actuelle", 0.0, 1.0, float(st.session_state.get("w_snow_cur", 0.0)), 0.01, key="s_snow_cur", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Min possible")
        snow_min = st.slider("Neige min", 0.0, 1.0, float(st.session_state.get("w_snow_min", 0.0)), 0.01, key="s_snow_min", label_visibility="collapsed")
    with c2:
        st.caption("Max possible")
        snow_max = st.slider("Neige max", 0.0, 1.0, float(st.session_state.get("w_snow_max", 0.0)), 0.01, key="s_snow_max", label_visibility="collapsed")
    if snow_max > 0:
        st.markdown('<div class="info-badge" style="border-color:rgba(100,180,255,0.4);">❄️ Neige activée — utilise ce préset uniquement sur Sakhal</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Storm
    st.markdown('<div class="weather-section">', unsafe_allow_html=True)
    st.markdown('<div class="weather-section-title">⛈️ Orages & Éclairs</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("Densité (0-1)")
        storm_density = st.slider("Densité", 0.0, 1.0, float(st.session_state.get("w_storm_density", 1.0)), 0.01, key="s_storm_density", label_visibility="collapsed")
    with c2:
        st.caption("Seuil overcast")
        storm_threshold = st.slider("Seuil", 0.0, 1.0, float(st.session_state.get("w_storm_threshold", 0.98)), 0.01, key="s_storm_threshold", label_visibility="collapsed")
    with c3:
        st.caption("Délai (sec)")
        storm_timeout = st.slider("Délai", 10, 300, int(st.session_state.get("w_storm_timeout", 45)), 5, key="s_storm_timeout", label_visibility="collapsed")
    st.markdown(f'<div class="info-badge">{"⚡ Orages fréquents" if storm_density > 0.7 else "🌩️ Orages occasionnels" if storm_density > 0.3 else "🌤️ Orages rares"} | 1 éclair toutes les <strong>{storm_timeout}s</strong> | Nécessite overcast > {storm_threshold:.2f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
#  PRÉVISUALISATION PLOTLY
# ─────────────────────────────────────────────
st.markdown("### 📊 Prévisualisation du cycle météo simulé")
st.caption("Simulation d'un cycle de 24h basée sur tes paramètres min/max")

import random
random.seed(42)

def simulate_weather_cycle(cur, w_min, w_max, steps=48):
    """Simule un cycle météo réaliste avec transitions douces."""
    values = [cur]
    for _ in range(steps - 1):
        target = random.uniform(w_min, w_max)
        # Transition douce vers la cible
        prev = values[-1]
        next_val = prev + (target - prev) * random.uniform(0.1, 0.4)
        next_val = max(w_min, min(w_max, next_val))
        values.append(round(next_val, 3))
    return values

hours = [f"{i//2:02d}h{'30' if i%2 else '00'}" for i in range(48)]

ov_vals   = simulate_weather_cycle(overcast_cur, overcast_min, overcast_max)
fog_vals  = simulate_weather_cycle(fog_cur, fog_min, fog_max)
rain_vals = simulate_weather_cycle(rain_cur, rain_min, rain_max)
wind_vals = simulate_weather_cycle(wind_cur, wind_min, wind_max)
snow_vals = simulate_weather_cycle(snow_cur, snow_min, snow_max)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=hours, y=ov_vals, name="☁️ Overcast",
    line=dict(color="#00D4FF", width=2.5),
    fill="tozeroy", fillcolor="rgba(0,212,255,0.06)"
))
fig.add_trace(go.Scatter(
    x=hours, y=fog_vals, name="🌫️ Brouillard",
    line=dict(color="#90CAF9", width=2, dash="dot"),
))
fig.add_trace(go.Scatter(
    x=hours, y=rain_vals, name="🌧️ Pluie",
    line=dict(color="#4FC3F7", width=2.5),
    fill="tozeroy", fillcolor="rgba(79,195,247,0.08)"
))
if snow_max > 0:
    fig.add_trace(go.Scatter(
        x=hours, y=snow_vals, name="❄️ Neige",
        line=dict(color="#B3E5FC", width=2, dash="dash"),
    ))

fig.add_trace(go.Scatter(
    x=hours, y=[v/20 for v in wind_vals], name="💨 Vent (÷20)",
    line=dict(color="#FFD600", width=1.5, dash="dot"),
    yaxis="y",
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0, 15, 30, 0.6)",
    font=dict(color="rgba(255,255,255,0.7)", family="Inter"),
    legend=dict(
        bgcolor="rgba(0,25,50,0.8)",
        bordercolor="rgba(0,212,255,0.3)",
        borderwidth=1,
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1
    ),
    xaxis=dict(
        gridcolor="rgba(0,212,255,0.08)",
        tickfont=dict(size=10),
        tickangle=45,
    ),
    yaxis=dict(
        gridcolor="rgba(0,212,255,0.08)",
        range=[0, 1.05],
        title=dict(text="Intensité (0-1)", font=dict(size=11)),
    ),
    height=320,
    margin=dict(l=50, r=20, t=40, b=60),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
#  GÉNÉRATION XML
# ─────────────────────────────────────────────
st.markdown("### 📄 Fichier généré")

def generate_xml(enable, reset, overcast_cur, overcast_min, overcast_max,
                 fog_cur, fog_min, fog_max,
                 rain_cur, rain_min, rain_max, rain_thresh_min, rain_thresh_max,
                 wind_cur, wind_min, wind_max, wind_dir,
                 snow_cur, snow_min, snow_max,
                 storm_density, storm_threshold, storm_timeout):

    enable_val = "1" if enable else "0"
    reset_val  = "1" if reset  else "0"

    # Timelimits et changelimits calculés intelligemment selon l'amplitude
    def timelimits(w_min, w_max):
        spread = w_max - w_min
        if spread < 0.1:
            return 900, 900
        elif spread < 0.5:
            return 300, 600
        else:
            return 120, 300

    ov_tmin, ov_tmax   = timelimits(overcast_min, overcast_max)
    fog_tmin, fog_tmax = timelimits(fog_min, fog_max)
    rain_tmin, rain_tmax = (60, 120) if rain_max > 0 else (300, 3600)

    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<!-- Généré par CodeX Suite — EpSy -->
<!-- 'reset' et 'enable' supportent : 0/1, true/false, yes/no -->
<weather reset="{reset_val}" enable="{enable_val}">

    <overcast>
        <!-- Conditions initiales : valeur cible, temps de transition, durée -->
        <current actual="{overcast_cur:.2f}" time="120" duration="240" />
        <!-- Plage de valeurs (0..1) -->
        <limits min="{overcast_min:.2f}" max="{overcast_max:.2f}" />
        <!-- Durée de transition entre deux états (secondes) -->
        <timelimits min="{ov_tmin}" max="{ov_tmax}" />
        <!-- Amplitude max du changement -->
        <changelimits min="0.0" max="{overcast_max - overcast_min:.2f}" />
    </overcast>

    <fog>
        <current actual="{fog_cur:.2f}" time="0" duration="32768" />
        <limits min="{fog_min:.2f}" max="{fog_max:.2f}" />
        <timelimits min="{fog_tmin}" max="{fog_tmax}" />
        <changelimits min="0.0" max="{max(fog_max - fog_min, 0.0):.2f}" />
    </fog>

    <rain>
        <current actual="{rain_cur:.2f}" time="0" duration="32768" />
        <limits min="{rain_min:.2f}" max="{rain_max:.2f}" />
        <timelimits min="{rain_tmin}" max="{rain_tmax}" />
        <changelimits min="0.0" max="{max(rain_max - rain_min, 0.0):.2f}" />
        <!-- Seuil d'overcast requis pour la pluie -->
        <thresholds min="{rain_thresh_min:.2f}" max="{rain_thresh_max:.2f}" end="120" />
    </rain>

    <windMagnitude>
        <current actual="{wind_cur:.1f}" time="120" duration="240" />
        <limits min="{wind_min:.1f}" max="{wind_max:.1f}" />
        <timelimits min="120" max="240" />
        <changelimits min="0.0" max="{max(wind_max - wind_min, 0.0):.1f}" />
    </windMagnitude>

    <windDirection>
        <current actual="{wind_dir:.2f}" time="120" duration="240" />
        <limits min="-3.14" max="3.14" />
        <timelimits min="60" max="120" />
        <changelimits min="-1.0" max="1.0" />
    </windDirection>

    <snowfall>
        <current actual="{snow_cur:.2f}" time="60" duration="120" />
        <limits min="{snow_min:.2f}" max="{snow_max:.2f}" />
        <timelimits min="60" max="120" />
        <changelimits min="0.0" max="{max(snow_max - snow_min, 0.0):.2f}" />
        <!-- Seuil d'overcast requis pour la neige -->
        <thresholds min="0.30" max="1.0" end="60" />
    </snowfall>

    <!-- Densité éclairs (0..1), seuil overcast, délai entre éclairs (secondes) -->
    <storm density="{storm_density:.2f}" threshold="{storm_threshold:.2f}" timeout="{storm_timeout}"/>

</weather>"""
    return xml

xml_content = generate_xml(
    enable, reset,
    overcast_cur, overcast_min, overcast_max,
    fog_cur, fog_min, fog_max,
    rain_cur, rain_min, rain_max, rain_thresh_min, rain_thresh_max,
    wind_cur, wind_min, wind_max, wind_dir,
    snow_cur, snow_min, snow_max,
    storm_density, storm_threshold, storm_timeout
)

# Aperçu coloré
xml_colored = xml_content
xml_colored = xml_colored.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

col_preview, col_dl = st.columns([3, 1])
with col_preview:
    st.markdown(f'<div class="xml-preview"><pre style="margin:0;white-space:pre-wrap;">{xml_content}</pre></div>', unsafe_allow_html=True)

with col_dl:
    st.markdown("<br><br>", unsafe_allow_html=True)
    preset_name = st.session_state.get("active_preset", "custom").lower().replace(" ", "_").replace("(", "").replace(")", "")
    st.download_button(
        label="📥 Télécharger\ncfgweather.xml",
        data=xml_content.encode("utf-8"),
        file_name="cfgweather.xml",
        mime="application/xml",
        use_container_width=True,
    )
    st.markdown(f'<div class="info-badge" style="margin-top:12px;">📌 Préset : <strong>{st.session_state.get("active_preset","Personnalisé")}</strong><br>⚠️ Mettre dans le dossier mission de ta map<br>🔄 Redémarre le serveur après upload</div>', unsafe_allow_html=True)
