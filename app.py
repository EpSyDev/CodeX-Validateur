"""
Codex Suite - Page d'accueil
HYBRID EDITION - Black × Glacier Blue
Créé par EpSy
"""

import streamlit as st

st.set_page_config(
    page_title="Codex Suite - Accueil",
    page_icon="images/favicon.png",  # TON LOGO ICI
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { 
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
}

/* FOND NOIR PUR */
.stApp {
    background: #000000;
    position: relative;
    overflow-x: hidden;
}

/* Particules de glace subtiles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 15% 20%, rgba(0, 212, 255, 0.03) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(56, 189, 248, 0.02) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.98);
    border-right: 1px solid rgba(0, 212, 255, 0.2);
}

/* HERO SECTION */
.hero-container {
    text-align: center;
    padding: 100px 20px 80px 20px;
    position: relative;
    z-index: 1;
}

/* Glow animé derrière le logo */
.hero-glow {
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
    filter: blur(80px);
    animation: pulse-glow 4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.4; transform: translateX(-50%) scale(1); }
    50% { opacity: 0.7; transform: translateX(-50%) scale(1.1); }
}

.logo-wrapper {
    margin-bottom: 40px;
}

.hero-title {
    font-size: 80px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF 0%, #38BDF8 50%, #0EA5E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    letter-spacing: -3px;
    line-height: 1;
    position: relative;
    display: inline-block;
}

.hero-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00D4FF, transparent);
    opacity: 0.5;
}

.hero-subtitle {
    font-size: 22px;
    color: rgba(0, 212, 255, 0.8);
    font-weight: 300;
    margin-bottom: 50px;
    letter-spacing: 1px;
}

.pills-row {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    margin-top: 40px;
}

.pill-badge {
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00D4FF;
    padding: 12px 24px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.pill-badge:hover {
    background: rgba(0, 212, 255, 0.15);
    border-color: rgba(0, 212, 255, 0.6);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
}

/* MODULES */
.modules-section {
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
    font-size: 12px;
    color: rgba(0, 212, 255, 0.7);
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.section-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
}

/* CARDS GLASSMORPHISM 3D */
.module-box {
    background: linear-gradient(135deg, rgba(0, 20, 40, 0.6) 0%, rgba(0, 10, 20, 0.7) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 28px;
    padding: 45px 35px;
    text-align: center;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

/* Bordure lumineuse animée */
.module-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #00D4FF, #38BDF8, #0EA5E9);
    opacity: 0;
    transition: opacity 0.4s ease;
}

/* Glow interne au hover */
.module-box::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300%;
    height: 300%;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.module-box:hover {
    transform: translateY(-12px) scale(1.02);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 
        0 20px 60px rgba(0, 212, 255, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.module-box:hover::before {
    opacity: 1;
}

.module-box:hover::after {
    opacity: 1;
}

.module-emoji {
    font-size: 68px;
    margin-bottom: 28px;
    filter: drop-shadow(0 4px 20px rgba(0, 212, 255, 0.4));
    transition: transform 0.4s ease;
    position: relative;
    z-index: 1;
}

.module-box:hover .module-emoji {
    transform: scale(1.1) rotate(-5deg);
}

.module-name {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 18px;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}

.module-desc {
    color: rgba(0, 212, 255, 0.8);
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 30px;
    font-weight: 300;
    position: relative;
    z-index: 1;
}

.module-list {
    text-align: left;
    margin-top: 25px;
    padding-top: 25px;
    border-top: 1px solid rgba(0, 212, 255, 0.15);
    position: relative;
    z-index: 1;
}

.feature-line {
    color: #00D4FF;
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
    color: #38BDF8;
    font-weight: 700;
}

/* STATS */
.stats-wrapper {
    background: rgba(0, 0, 0, 0.5);
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    padding: 80px 30px;
    margin: 100px 0;
    position: relative;
    z-index: 1;
}

.stat-box {
    text-align: center;
    padding: 35px 25px;
    background: rgba(0, 20, 40, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 20px;
    backdrop-filter: blur(15px);
    transition: all 0.3s ease;
}

.stat-box:hover {
    border-color: rgba(0, 212, 255, 0.4);
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2);
}

.stat-number {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
    letter-spacing: -2px;
}

.stat-label {
    color: rgba(0, 212, 255, 0.7);
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ROADMAP */
.roadmap-section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 80px 30px;
    position: relative;
    z-index: 1;
}

.roadmap-box {
    background: rgba(0, 20, 40, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 24px;
    padding: 45px;
    backdrop-filter: blur(15px);
}

.roadmap-heading {
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 30px;
}

.roadmap-item {
    color: #64748b;
    font-size: 16px;
    margin: 16px 0;
    padding-left: 32px;
    position: relative;
}

.roadmap-item.complete {
    color: #00D4FF;
    font-weight: 500;
}

.roadmap-item.progress {
    color: #fbbf24;
    font-weight: 500;
}

.roadmap-item.complete::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #00D4FF;
    font-size: 20px;
    font-weight: 900;
}

.roadmap-item.progress::before {
    content: '⟳';
    position: absolute;
    left: 0;
    color: #fbbf24;
    font-size: 20px;
}

/* FOOTER */
.footer-area {
    text-align: center;
    padding: 70px 30px 50px 30px;
    margin-top: 100px;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    position: relative;
    z-index: 1;
}

.footer-brand {
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

.footer-text {
    color: #64748b;
    font-size: 14px;
    margin: 10px 0;
}

.footer-nav {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
}

.footer-link {
    color: #00D4FF;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.footer-link:hover {
    color: #38BDF8;
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    letter-spacing: 0.5px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0, 212, 255, 0.5);
    background: linear-gradient(135deg, #38BDF8 0%, #00D4FF 100%);
}

@media (max-width: 768px) {
    .hero-title { font-size: 52px; }
    .hero-subtitle { font-size: 18px; }
    .module-name { font-size: 24px; }
    .section-title { font-size: 34px; }
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero-container">
    <div class="hero-glow"></div>
    <div class="logo-wrapper">
        <img src="app/static/codex3-V2.png" style="max-width: 200px; filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.4));">
    </div>
    <h1 class="hero-title">CODEX SUITE</h1>
    <p class="hero-subtitle">La boîte à outils ultime pour DayZ</p>
    <div class="pills-row">
        <span class="pill-badge">🔍 VALIDATION AUTO</span>
        <span class="pill-badge">🗺️ ÉDITEUR VISUEL</span>
        <span class="pill-badge">📚 DOCUMENTATION</span>
        <span class="pill-badge">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# MODULES
st.markdown('<div class="modules-section">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-label">Modules disponibles</div>
    <h2 class="section-title">Choisis ton outil</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="module-box">
        <div class="module-emoji">📝</div>
        <div class="module-name">Validateur</div>
        <div class="module-desc">Valide et corrige automatiquement tes fichiers de configuration DayZ</div>
        <div class="module-list">
            <div class="feature-line">Détection erreurs</div>
            <div class="feature-line">Correction automatique</div>
            <div class="feature-line">Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🚀 Ouvrir", key="btn_val"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("""
    <div class="module-box">
        <div class="module-emoji">🗺️</div>
        <div class="module-name">Carte Interactive</div>
        <div class="module-desc">Édite visuellement les spawns zombies sur les cartes DayZ</div>
        <div class="module-list">
            <div class="feature-line">Chernarus</div>
            <div class="feature-line">Livonia</div>
            <div class="feature-line">Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗺️ Ouvrir", key="btn_map"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="module-box">
        <div class="module-emoji">📚</div>
        <div class="module-name">Documentation</div>
        <div class="module-desc">Apprends à maîtriser les fichiers de configuration DayZ</div>
        <div class="module-list">
            <div class="feature-line">types.xml</div>
            <div class="feature-line">events.xml</div>
            <div class="feature-line">economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir", key="btn_doc"):
        st.switch_page("pages/3_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# STATS
st.markdown('<div class="stats-wrapper">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-label">Chiffres clés</div>
    <h2 class="section-title">Codex en action</h2>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-number">5+</div><div class="stat-label">Fichiers</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-number">100%</div><div class="stat-label">Auto</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-box"><div class="stat-number">3</div><div class="stat-label">Maps</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-box"><div class="stat-number">170+</div><div class="stat-label">Docs</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ROADMAP
st.markdown('<div class="roadmap-section">', unsafe_allow_html=True)
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
        <div class="roadmap-item complete">Validateur XML/JSON</div>
        <div class="roadmap-item complete">Correction auto</div>
        <div class="roadmap-item complete">Validation sémantique</div>
        <div class="roadmap-item complete">Documentation</div>
        <div class="roadmap-item complete">Carte Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-box">
        <div class="roadmap-heading">🚧 En cours</div>
        <div class="roadmap-item progress">Calibration Chernarus</div>
        <div class="roadmap-item progress">Calibration Sakhal</div>
        <div class="roadmap-item progress">Éditeur types.xml</div>
        <div class="roadmap-item progress">Templates</div>
        <div class="roadmap-item progress">Chatbot IA</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer-area">
    <div class="footer-brand">CODEX SUITE v3.0</div>
    <p class="footer-text">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div class="footer-nav">
        <a href="https://discord.gg/CQR6KTJ63C" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
