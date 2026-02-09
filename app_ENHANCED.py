"""
Codex Suite - HYBRID ENHANCED
Black × Glacier Blue avec effets premium
Créé par EpSy
"""

import streamlit as st

st.set_page_config(
    page_title="Codex Suite",
    page_icon="images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { 
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #000000;
    position: relative;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Particules subtiles en fond */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.02) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(56, 189, 248, 0.015) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* HERO SECTION */
.hero-box {
    text-align: center;
    padding: 100px 20px 70px 20px;
    position: relative;
    z-index: 1;
}

/* Glow pulsant subtil derrière titre */
.hero-box::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.08) 0%, transparent 70%);
    filter: blur(60px);
    animation: pulse 4s ease-in-out infinite;
    z-index: -1;
}

@keyframes pulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.6; }
}

.hero-title {
    font-size: 76px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF 0%, #38BDF8 50%, #0EA5E9 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    letter-spacing: -2px;
    animation: gradient-shift 8s ease infinite;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
}

@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.hero-sub {
    font-size: 22px;
    color: rgba(0, 212, 255, 0.9);
    margin-bottom: 45px;
    letter-spacing: 0.5px;
}

.pills-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
}

.pill {
    display: inline-block;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00D4FF;
    padding: 11px 22px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    margin: 5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.pill:hover {
    background: rgba(0, 212, 255, 0.15);
    border-color: rgba(0, 212, 255, 0.6);
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.25);
}

/* MODULES SECTION */
.modules-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 30px;
}

.section-title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 50px;
}

/* CARDS PREMIUM */
.card {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.6) 0%, rgba(0, 15, 30, 0.7) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 26px;
    padding: 42px 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Bordure top animée */
.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00D4FF, transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}

/* Glow interne au hover */
.card::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.08) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.card:hover {
    transform: translateY(-10px);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 
        0 20px 50px rgba(0, 212, 255, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.card:hover::before {
    opacity: 1;
}

.card:hover::after {
    opacity: 1;
}

.card-icon {
    font-size: 64px;
    margin-bottom: 24px;
    filter: drop-shadow(0 4px 15px rgba(0, 212, 255, 0.3));
    transition: transform 0.4s ease;
    position: relative;
    z-index: 1;
}

.card:hover .card-icon {
    transform: scale(1.1) rotate(-5deg);
}

.card-title {
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}

.card-text {
    color: rgba(0, 212, 255, 0.8);
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 24px;
    position: relative;
    z-index: 1;
}

.card-list {
    text-align: left;
    margin-top: 22px;
    padding-top: 22px;
    border-top: 1px solid rgba(0, 212, 255, 0.12);
    position: relative;
    z-index: 1;
}

.list-line {
    color: #00D4FF;
    font-size: 13px;
    margin: 10px 0;
    padding-left: 20px;
    position: relative;
    transition: transform 0.2s ease;
}

.list-line::before {
    content: '→';
    position: absolute;
    left: 0;
    transition: transform 0.2s ease;
}

.card:hover .list-line::before {
    transform: translateX(3px);
}

/* STATS SECTION */
.stats-section {
    background: rgba(0, 0, 0, 0.4);
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    padding: 70px 30px;
    margin: 90px 0;
}

.stat {
    text-align: center;
    padding: 32px 22px;
    background: rgba(0, 25, 50, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 18px;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}

.stat:hover {
    border-color: rgba(0, 212, 255, 0.4);
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0, 212, 255, 0.2);
}

.stat-num {
    font-size: 50px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    letter-spacing: -1px;
}

.stat-label {
    color: rgba(0, 212, 255, 0.7);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ROADMAP */
.roadmap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 70px 30px;
}

.roadmap-card {
    background: rgba(0, 25, 50, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 22px;
    padding: 42px;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.roadmap-card:hover {
    border-color: rgba(0, 212, 255, 0.35);
    box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15);
}

.roadmap-title {
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 26px;
}

.roadmap-item {
    color: #64748b;
    font-size: 15px;
    margin: 13px 0;
    padding-left: 30px;
    position: relative;
    transition: all 0.2s ease;
}

.roadmap-item.done {
    color: #00D4FF;
}

.roadmap-item.wip {
    color: #fbbf24;
}

.roadmap-item.done::before {
    content: '✓';
    position: absolute;
    left: 0;
    font-size: 18px;
    font-weight: 900;
}

.roadmap-item.wip::before {
    content: '⟳';
    position: absolute;
    left: 0;
    font-size: 18px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.roadmap-card:hover .roadmap-item {
    transform: translateX(3px);
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 65px 30px 45px 30px;
    margin-top: 90px;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
}

.footer-brand {
    font-size: 21px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.footer-text {
    color: #64748b;
    font-size: 13px;
    margin: 8px 0;
}

.footer-link {
    color: #00D4FF;
    text-decoration: none;
    margin: 0 16px;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.footer-link:hover {
    color: #38BDF8;
    text-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
    border: none;
    border-radius: 13px;
    padding: 15px 30px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.25);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(0, 212, 255, 0.4);
    background: linear-gradient(135deg, #38BDF8 0%, #00D4FF 100%);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .hero-title { font-size: 50px; }
    .hero-sub { font-size: 18px; }
    .card-title { font-size: 22px; }
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero-box">
    <h1 class="hero-title">CODEX SUITE</h1>
    <p class="hero-sub">La boîte à outils ultime pour DayZ</p>
    <div class="pills-row">
        <span class="pill">🔍 VALIDATION AUTO</span>
        <span class="pill">🗺️ ÉDITEUR VISUEL</span>
        <span class="pill">📚 DOCUMENTATION</span>
        <span class="pill">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# MODULES
st.markdown('<div class="modules-wrapper">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🚀 Modules disponibles</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📝</div>
        <div class="card-title">Validateur</div>
        <div class="card-text">Valide et corrige automatiquement tes fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-line">Détection erreurs</div>
            <div class="list-line">Correction automatique</div>
            <div class="list-line">Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🚀 Ouvrir", key="v"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🗺️</div>
        <div class="card-title">Carte Interactive</div>
        <div class="card-text">Édite visuellement les spawns zombies sur les cartes DayZ</div>
        <div class="card-list">
            <div class="list-line">Chernarus</div>
            <div class="list-line">Livonia</div>
            <div class="list-line">Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗺️ Ouvrir", key="m"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📚</div>
        <div class="card-title">Documentation</div>
        <div class="card-text">Apprends à maîtriser les fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-line">types.xml</div>
            <div class="list-line">events.xml</div>
            <div class="list-line">economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir", key="d"):
        st.switch_page("pages/3_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# STATS
st.markdown('<div class="stats-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Codex en chiffres</h2>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat"><div class="stat-num">5+</div><div class="stat-label">Fichiers</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat"><div class="stat-num">100%</div><div class="stat-label">Auto</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat"><div class="stat-num">3</div><div class="stat-label">Maps</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat"><div class="stat-num">170+</div><div class="stat-label">Docs</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ROADMAP
st.markdown('<div class="roadmap">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🛣️ Roadmap</h2>', unsafe_allow_html=True)

r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">✅ Disponible</div>
        <div class="roadmap-item done">Validateur XML/JSON</div>
        <div class="roadmap-item done">Correction automatique</div>
        <div class="roadmap-item done">Validation sémantique</div>
        <div class="roadmap-item done">Documentation</div>
        <div class="roadmap-item done">Carte Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">🚧 En cours</div>
        <div class="roadmap-item wip">Calibration Chernarus</div>
        <div class="roadmap-item wip">Calibration Sakhal</div>
        <div class="roadmap-item wip">Éditeur types.xml</div>
        <div class="roadmap-item wip">Templates</div>
        <div class="roadmap-item wip">Chatbot IA</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <div class="footer-brand">CODEX SUITE v3.0</div>
    <p class="footer-text">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div style="margin-top: 22px;">
        <a href="https://discord.gg/CQR6KTJ63C" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
