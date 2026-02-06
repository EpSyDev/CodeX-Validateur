"""
Codex Suite - Page d'accueil
Arctic Blue Edition v3.0 - Premium
Créé par EpSy
"""

import streamlit as st

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Codex Suite - Accueil",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS ARCTIC - STABLE
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { 
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
}

.stApp {
    background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #0d1b2a 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stSidebar"] {
    background: rgba(15, 20, 25, 0.98);
    border-right: 1px solid rgba(99, 179, 237, 0.2);
}

.hero-wrapper {
    text-align: center;
    padding: 100px 20px 80px 20px;
    position: relative;
}

.hero-label {
    font-size: 20px;
    color: #7dd3fc;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 30px;
    text-transform: uppercase;
}

.hero-main {
    font-size: 80px;
    font-weight: 900;
    background: linear-gradient(135deg, #bae6fd 0%, #7dd3fc 30%, #38bdf8 60%, #0ea5e9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 25px;
    letter-spacing: -3px;
    line-height: 1.1;
}

.hero-desc {
    font-size: 22px;
    color: #bae6fd;
    font-weight: 300;
    margin-bottom: 50px;
    letter-spacing: 0.5px;
}

.pills-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 40px;
}

.badge-pill {
    background: rgba(14, 165, 233, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #bae6fd;
    padding: 10px 22px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
}

.modules-zone {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 30px;
}

.section-top {
    text-align: center;
    margin-bottom: 60px;
}

.section-mini {
    font-size: 13px;
    color: #7dd3fc;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.section-big {
    font-size: 42px;
    font-weight: 800;
    color: #f0f9ff;
    letter-spacing: -1px;
}

.card-module {
    background: linear-gradient(135deg, rgba(26, 35, 50, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 28px;
    padding: 45px 35px;
    text-align: center;
    height: 100%;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.card-icon {
    font-size: 68px;
    margin-bottom: 28px;
}

.card-name {
    font-size: 28px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 18px;
    letter-spacing: -0.5px;
}

.card-info {
    color: #bae6fd;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 30px;
    font-weight: 300;
}

.card-list {
    text-align: left;
    margin-top: 25px;
    padding-top: 25px;
    border-top: 1px solid rgba(56, 189, 248, 0.15);
}

.list-item {
    color: #7dd3fc;
    font-size: 14px;
    margin: 12px 0;
    padding-left: 24px;
    position: relative;
    font-weight: 500;
}

.stats-zone {
    background: rgba(15, 20, 25, 0.6);
    border-top: 1px solid rgba(56, 189, 248, 0.2);
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding: 80px 30px;
    margin: 100px 0;
}

.stat-item {
    text-align: center;
    padding: 35px 25px;
    background: rgba(26, 35, 50, 0.5);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 20px;
}

.stat-num {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(135deg, #bae6fd, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.stat-text {
    color: #7dd3fc;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.roadmap-zone {
    max-width: 1200px;
    margin: 0 auto;
    padding: 80px 30px;
}

.roadmap-card {
    background: rgba(26, 35, 50, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 24px;
    padding: 45px;
}

.roadmap-title {
    font-size: 26px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 30px;
}

.roadmap-line {
    color: #94a3b8;
    font-size: 16px;
    margin: 16px 0;
    padding-left: 32px;
    position: relative;
}

.roadmap-line.done {
    color: #7dd3fc;
    font-weight: 500;
}

.roadmap-line.wip {
    color: #fbbf24;
    font-weight: 500;
}

.footer-zone {
    text-align: center;
    padding: 70px 30px 50px 30px;
    margin-top: 100px;
    border-top: 1px solid rgba(56, 189, 248, 0.2);
}

.footer-name {
    font-size: 22px;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

.footer-line {
    color: #64748b;
    font-size: 14px;
    margin: 10px 0;
}

.footer-links {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
}

.footer-link {
    color: #7dd3fc;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white;
    border: 1px solid rgba(186, 230, 253, 0.2);
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3);
    letter-spacing: 0.5px;
}

@media (max-width: 768px) {
    .hero-main { font-size: 52px; }
    .hero-desc { font-size: 18px; }
    .card-name { font-size: 24px; }
    .section-big { font-size: 34px; }
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HERO
# ==============================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-label">❄️ CODEX</div>
    <h1 class="hero-main">SUITE</h1>
    <p class="hero-desc">La boîte à outils ultime pour DayZ</p>
    <div class="pills-container">
        <span class="badge-pill">🔍 VALIDATION AUTO</span>
        <span class="badge-pill">🗺️ ÉDITEUR VISUEL</span>
        <span class="badge-pill">📚 DOCUMENTATION</span>
        <span class="badge-pill">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================
# MODULES
# ==============================
st.markdown('<div class="modules-zone">', unsafe_allow_html=True)
st.markdown("""
<div class="section-top">
    <div class="section-mini">Modules disponibles</div>
    <h2 class="section-big">Choisis ton outil</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="card-module">
        <div class="card-icon">📝</div>
        <div class="card-name">Validateur</div>
        <div class="card-info">Valide et corrige automatiquement tes fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-item">→ Détection erreurs</div>
            <div class="list-item">→ Correction automatique</div>
            <div class="list-item">→ Validation sémantique</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🚀 Ouvrir le Validateur", key="btn_val"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("""
    <div class="card-module">
        <div class="card-icon">🗺️</div>
        <div class="card-name">Carte Interactive</div>
        <div class="card-info">Édite visuellement les spawns zombies sur les cartes DayZ</div>
        <div class="card-list">
            <div class="list-item">→ Chernarus</div>
            <div class="list-item">→ Livonia</div>
            <div class="list-item">→ Sakhal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗺️ Ouvrir la Carte", key="btn_map"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("""
    <div class="card-module">
        <div class="card-icon">📚</div>
        <div class="card-name">Documentation</div>
        <div class="card-info">Apprends à maîtriser les fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-item">→ types.xml</div>
            <div class="list-item">→ events.xml</div>
            <div class="list-item">→ economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir la Doc", key="btn_doc"):
        st.switch_page("pages/3_Documentation.py")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# STATS
# ==============================
st.markdown('<div class="stats-zone">', unsafe_allow_html=True)
st.markdown("""
<div class="section-top">
    <div class="section-mini">Chiffres clés</div>
    <h2 class="section-big">Codex en action</h2>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-item"><div class="stat-num">5+</div><div class="stat-text">Fichiers supportés</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-item"><div class="stat-num">100%</div><div class="stat-text">Corrections auto</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-item"><div class="stat-num">3</div><div class="stat-text">Maps disponibles</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-item"><div class="stat-num">170+</div><div class="stat-text">Pages de doc</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# ROADMAP
# ==============================
st.markdown('<div class="roadmap-zone">', unsafe_allow_html=True)
st.markdown("""
<div class="section-top">
    <div class="section-mini">Développement</div>
    <h2 class="section-big">Roadmap</h2>
</div>
""", unsafe_allow_html=True)

r1, r2 = st.columns(2, gap="large")

with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">✅ Disponible</div>
        <div class="roadmap-line done">✓ Validateur XML/JSON complet</div>
        <div class="roadmap-line done">✓ Correction automatique</div>
        <div class="roadmap-line done">✓ Validation sémantique</div>
        <div class="roadmap-line done">✓ Documentation exhaustive</div>
        <div class="roadmap-line done">✓ Carte interactive Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">🚧 En développement</div>
        <div class="roadmap-line wip">⟳ Calibration Chernarus</div>
        <div class="roadmap-line wip">⟳ Calibration Sakhal</div>
        <div class="roadmap-line wip">⟳ Éditeur types.xml</div>
        <div class="roadmap-line wip">⟳ Templates préconfigurés</div>
        <div class="roadmap-line wip">⟳ Export multi-format</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer-zone">
    <div class="footer-name">CODEX SUITE v3.0</div>
    <p class="footer-line">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div class="footer-links">
        <a href="https://discord.gg/CQR6KTJ63C" target="_blank" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" target="_blank" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
