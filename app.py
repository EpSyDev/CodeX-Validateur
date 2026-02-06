"""
Codex Suite - Page d'accueil
La boîte à outils DayZ francophone
Créé par EpSy

🎨 ARCTIC BLUE EDITION - Premium Glacier Theme
"""

import streamlit as st

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Suite - Accueil",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS CUSTOM - ARCTIC BLUE PREMIUM
# ==============================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

/* GLOBAL */
* { 
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
}

/* Main background - Arctic gradient */
.stApp {
    background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #0d1b2a 100%);
    position: relative;
}

/* Animated particles effect */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(99, 179, 237, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(186, 230, 253, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(147, 197, 253, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 20, 25, 0.98);
    border-right: 1px solid rgba(99, 179, 237, 0.2);
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] * {
    color: #e0f2fe !important;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 100px 20px 80px 20px;
    position: relative;
    z-index: 1;
}

.hero-frost {
    position: absolute;
    top: -30%;
    left: 50%;
    transform: translateX(-50%);
    width: 1000px;
    height: 1000px;
    background: radial-gradient(circle, rgba(186, 230, 253, 0.15) 0%, transparent 60%);
    filter: blur(100px);
    pointer-events: none;
    animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; transform: translateX(-50%) scale(1); }
    50% { opacity: 0.8; transform: translateX(-50%) scale(1.1); }
}

.hero-logo {
    font-size: 24px;
    color: #7dd3fc;
    font-weight: 600;
    letter-spacing: 3px;
    margin-bottom: 30px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 80px;
    font-weight: 900;
    background: linear-gradient(135deg, #bae6fd 0%, #7dd3fc 30%, #38bdf8 60%, #0ea5e9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 25px;
    letter-spacing: -3px;
    line-height: 1.1;
    filter: drop-shadow(0 0 30px rgba(56, 189, 248, 0.3));
}

.hero-subtitle {
    font-size: 22px;
    color: #bae6fd;
    font-weight: 300;
    margin-bottom: 50px;
    letter-spacing: 0.5px;
}

.feature-pills {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 40px;
}

.pill {
    background: rgba(14, 165, 233, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #bae6fd;
    padding: 10px 22px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.5px;
}

.pill:hover {
    background: rgba(14, 165, 233, 0.2);
    border-color: rgba(56, 189, 248, 0.6);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(56, 189, 248, 0.25);
}

/* Modules Grid */
.modules-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 30px;
    position: relative;
    z-index: 1;
}

.section-header {
    text-align: center;
    margin-bottom: 60px;
}

.section-label {
    font-size: 13px;
    color: #7dd3fc;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.section-title {
    font-size: 42px;
    font-weight: 800;
    color: #f0f9ff;
    letter-spacing: -1px;
}

/* Module Cards - Frosted Glass */
.module-card {
    background: linear-gradient(135deg, rgba(26, 35, 50, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 28px;
    padding: 45px 35px;
    text-align: center;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.module-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #bae6fd, #38bdf8, #0ea5e9);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.module-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.module-card:hover::before {
    opacity: 1;
}

.module-card:hover::after {
    opacity: 1;
}

.module-card:hover {
    transform: translateY(-12px);
    border-color: rgba(56, 189, 248, 0.5);
    box-shadow: 
        0 20px 60px rgba(56, 189, 248, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    background: linear-gradient(135deg, rgba(26, 35, 50, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
}

.module-icon {
    font-size: 68px;
    margin-bottom: 28px;
    filter: drop-shadow(0 4px 20px rgba(56, 189, 248, 0.4));
    transition: transform 0.4s ease;
}

.module-card:hover .module-icon {
    transform: scale(1.1) rotate(-5deg);
}

.module-title {
    font-size: 28px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 18px;
    letter-spacing: -0.5px;
}

.module-description {
    color: #bae6fd;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 30px;
    font-weight: 300;
}

.module-features {
    text-align: left;
    margin-top: 25px;
    padding-top: 25px;
    border-top: 1px solid rgba(56, 189, 248, 0.15);
}

.feature-line {
    color: #7dd3fc;
    font-size: 14px;
    margin: 12px 0;
    padding-left: 24px;
    position: relative;
    font-weight: 500;
}

.feature-line::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #38bdf8;
    font-weight: 700;
}

/* Stats Section */
.stats-wrapper {
    background: rgba(15, 20, 25, 0.6);
    border-top: 1px solid rgba(56, 189, 248, 0.2);
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding: 80px 30px;
    margin: 100px 0;
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 1;
}

.stat-box {
    text-align: center;
    padding: 35px 25px;
    background: rgba(26, 35, 50, 0.5);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 20px;
    backdrop-filter: blur(15px);
    transition: all 0.3s ease;
}

.stat-box:hover {
    border-color: rgba(56, 189, 248, 0.4);
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2);
}

.stat-value {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(135deg, #bae6fd, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
    letter-spacing: -2px;
}

.stat-name {
    color: #7dd3fc;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* Roadmap */
.roadmap-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 80px 30px;
    position: relative;
    z-index: 1;
}

.roadmap-box {
    background: rgba(26, 35, 50, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 24px;
    padding: 45px;
    backdrop-filter: blur(15px);
}

.roadmap-heading {
    font-size: 26px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 30px;
    letter-spacing: -0.5px;
}

.roadmap-entry {
    color: #94a3b8;
    font-size: 16px;
    margin: 16px 0;
    padding-left: 32px;
    position: relative;
    font-weight: 400;
}

.roadmap-entry.active {
    color: #7dd3fc;
    font-weight: 500;
}

.roadmap-entry.progress {
    color: #fbbf24;
    font-weight: 500;
}

.roadmap-entry.active::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #38bdf8;
    font-size: 20px;
    font-weight: 900;
}

.roadmap-entry.progress::before {
    content: '⟳';
    position: absolute;
    left: 0;
    color: #fbbf24;
    font-size: 20px;
}

/* Footer */
.footer-section {
    text-align: center;
    padding: 70px 30px 50px 30px;
    margin-top: 100px;
    border-top: 1px solid rgba(56, 189, 248, 0.2);
    position: relative;
    z-index: 1;
}

.footer-brand {
    font-size: 22px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

.footer-info {
    color: #64748b;
    font-size: 14px;
    margin: 10px 0;
    font-weight: 400;
}

.footer-nav {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
}

.footer-anchor {
    color: #7dd3fc;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}

.footer-anchor:hover {
    color: #38bdf8;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white;
    border: 1px solid rgba(186, 230, 253, 0.2);
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 16px;
    font-weight: 700;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(14, 165, 233, 0.5);
    background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    border-color: rgba(186, 230, 253, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title { font-size: 52px; }
    .hero-subtitle { font-size: 18px; }
    .module-title { font-size: 24px; }
    .section-title { font-size: 34px; }
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div class="hero-section">
    <div class="hero-frost"></div>
    <div class="hero-logo">❄️ CODEX</div>
    <h1 class="hero-title">SUITE</h1>
    <p class="hero-subtitle">La boîte à outils ultime pour DayZ</p>
    <div class="feature-pills">
        <span class="pill">🔍 VALIDATION AUTO</span>
        <span class="pill">🗺️ ÉDITEUR VISUEL</span>
        <span class="pill">📚 DOCUMENTATION</span>
        <span class="pill">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================
# MODULES
# ==============================
st.markdown('<div class="modules-container">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-label">Modules disponibles</div>
    <h2 class="section-title">Choisis ton outil</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📝</div>
        <div class="module-title">Validateur</div>
        <div class="module-description">
            Valide et corrige automatiquement tes fichiers de configuration DayZ
        </div>
        <div class="module-features">
            <div class="feature-line">Détection erreurs</div>
            <div class="feature-line">Correction automatique</div>
            <div class="feature-line">Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🚀 Ouvrir", key="btn_val"):
        st.switch_page("pages/1_📝_Validateur.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🗺️</div>
        <div class="module-title">Carte Interactive</div>
        <div class="module-description">
            Édite visuellement les spawns zombies sur les cartes DayZ
        </div>
        <div class="module-features">
            <div class="feature-line">Chernarus</div>
            <div class="feature-line">Livonia</div>
            <div class="feature-line">Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗺️ Ouvrir", key="btn_map"):
        st.switch_page("pages/2_🗺️_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">📚</div>
        <div class="module-title">Documentation</div>
        <div class="module-description">
            Apprends à maîtriser les fichiers de configuration DayZ
        </div>
        <div class="module-features">
            <div class="feature-line">types.xml</div>
            <div class="feature-line">events.xml</div>
            <div class="feature-line">economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir", key="btn_doc"):
        st.switch_page("pages/3_📚_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# STATS
# ==============================
st.markdown('<div class="stats-wrapper">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-label">Chiffres clés</div>
    <h2 class="section-title">Codex en action</h2>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-value">5+</div><div class="stat-name">Fichiers supportés</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-value">100%</div><div class="stat-name">Corrections auto</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-box"><div class="stat-value">3</div><div class="stat-name">Maps disponibles</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-box"><div class="stat-value">170+</div><div class="stat-name">Pages de doc</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# ROADMAP
# ==============================
st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-label">Développement</div>
    <h2 class="section-title">Roadmap</h2>
</div>
""", unsafe_allow_html=True)

r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown("""
    <div class="roadmap-box">
        <div class="roadmap-heading">✅ Disponible</div>
        <div class="roadmap-entry active">Validateur XML/JSON complet</div>
        <div class="roadmap-entry active">Correction automatique</div>
        <div class="roadmap-entry active">Validation sémantique</div>
        <div class="roadmap-entry active">Documentation exhaustive</div>
        <div class="roadmap-entry active">Carte interactive Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-box">
        <div class="roadmap-heading">🚧 En développement</div>
        <div class="roadmap-entry progress">Calibration Chernarus</div>
        <div class="roadmap-entry progress">Calibration Sakhal</div>
        <div class="roadmap-entry progress">Éditeur types.xml</div>
        <div class="roadmap-entry progress">Templates préconfigurés</div>
        <div class="roadmap-entry progress">Export multi-format</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer-section">
    <div class="footer-brand">CODEX SUITE v3.0</div>
    <p class="footer-info">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div class="footer-nav">
        <a href="https://discord.gg/CQR6KTJ63C" target="_blank" class="footer-anchor">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" target="_blank" class="footer-anchor">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-anchor">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
