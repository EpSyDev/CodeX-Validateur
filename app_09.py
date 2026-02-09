"""
Codex Suite - HYBRID Black × Glacier Blue
Version progressive stable
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
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* HERO */
.hero-box {
    text-align: center;
    padding: 80px 20px 60px 20px;
}

.hero-title {
    font-size: 72px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF 0%, #38BDF8 50%, #0EA5E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    letter-spacing: -2px;
}

.hero-sub {
    font-size: 20px;
    color: #00D4FF;
    margin-bottom: 40px;
}

.pill {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00D4FF;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    margin: 5px;
}

/* CARDS */
.card {
    background: rgba(0, 30, 60, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 24px;
    padding: 40px 30px;
    text-align: center;
    transition: all 0.3s ease;
}

.card:hover {
    border-color: rgba(0, 212, 255, 0.5);
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 212, 255, 0.3);
}

.card-icon {
    font-size: 60px;
    margin-bottom: 20px;
}

.card-title {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 15px;
}

.card-text {
    color: rgba(0, 212, 255, 0.8);
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.card-list {
    text-align: left;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(0, 212, 255, 0.15);
}

.list-line {
    color: #00D4FF;
    font-size: 13px;
    margin: 8px 0;
    padding-left: 20px;
}

/* STATS */
.stats-section {
    background: rgba(0, 0, 0, 0.5);
    border-top: 1px solid rgba(0, 212, 255, 0.2);
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
    padding: 60px 30px;
    margin: 80px 0;
}

.stat {
    text-align: center;
    padding: 30px 20px;
    background: rgba(0, 30, 60, 0.4);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 16px;
}

.stat-num {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #00D4FF, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.stat-label {
    color: rgba(0, 212, 255, 0.7);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}

/* ROADMAP */
.roadmap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 60px 30px;
}

.roadmap-card {
    background: rgba(0, 30, 60, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    padding: 40px;
}

.roadmap-title {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 25px;
}

.roadmap-item {
    color: #64748b;
    font-size: 15px;
    margin: 12px 0;
    padding-left: 28px;
}

.roadmap-item.done {
    color: #00D4FF;
}

.roadmap-item.wip {
    color: #fbbf24;
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 60px 30px 40px 30px;
    margin-top: 80px;
    border-top: 1px solid rgba(0, 212, 255, 0.2);
}

.footer-brand {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 10px;
}

.footer-text {
    color: #64748b;
    font-size: 13px;
    margin: 8px 0;
}

.footer-link {
    color: #00D4FF;
    text-decoration: none;
    margin: 0 15px;
    font-size: 13px;
    font-weight: 600;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00D4FF, #0EA5E9);
    color: #000000;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
}

@media (max-width: 768px) {
    .hero-title { font-size: 48px; }
    .hero-sub { font-size: 16px; }
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero-box">
    <h1 class="hero-title">CODEX SUITE</h1>
    <p class="hero-sub">La boîte à outils ultime pour DayZ</p>
    <div>
        <span class="pill">🔍 VALIDATION AUTO</span>
        <span class="pill">🗺️ ÉDITEUR VISUEL</span>
        <span class="pill">📚 DOCUMENTATION</span>
        <span class="pill">🇫🇷 100% FRANÇAIS</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# MODULES
st.markdown("## 🚀 Modules disponibles")
st.markdown("")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📝</div>
        <div class="card-title">Validateur</div>
        <div class="card-text">Valide et corrige automatiquement tes fichiers de configuration DayZ</div>
        <div class="card-list">
            <div class="list-line">→ Détection erreurs</div>
            <div class="list-line">→ Correction auto</div>
            <div class="list-line">→ Validation sémantique</div>
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
            <div class="list-line">→ Chernarus</div>
            <div class="list-line">→ Livonia</div>
            <div class="list-line">→ Sakhal</div>
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
            <div class="list-line">→ types.xml</div>
            <div class="list-line">→ events.xml</div>
            <div class="list-line">→ economy.xml</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("📖 Ouvrir", key="d"):
        st.switch_page("pages/3_Documentation.py")

# STATS
st.markdown('<div class="stats-section">', unsafe_allow_html=True)
st.markdown("## 📊 Codex en chiffres")

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
st.markdown("## 🛣️ Roadmap")

r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">✅ Disponible</div>
        <div class="roadmap-item done">✓ Validateur XML/JSON</div>
        <div class="roadmap-item done">✓ Correction auto</div>
        <div class="roadmap-item done">✓ Validation sémantique</div>
        <div class="roadmap-item done">✓ Documentation</div>
        <div class="roadmap-item done">✓ Carte Livonia</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="roadmap-card">
        <div class="roadmap-title">🚧 En cours</div>
        <div class="roadmap-item wip">⟳ Calibration Chernarus</div>
        <div class="roadmap-item wip">⟳ Calibration Sakhal</div>
        <div class="roadmap-item wip">⟳ Éditeur types.xml</div>
        <div class="roadmap-item wip">⟳ Templates</div>
        <div class="roadmap-item wip">⟳ Chatbot IA</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <div class="footer-brand">CODEX SUITE v3.0</div>
    <p class="footer-text">Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
    <div style="margin-top: 20px;">
        <a href="https://discord.gg/CQR6KTJ63C" class="footer-link">💬 Discord</a>
        <a href="https://github.com/EpSyDev/codex-validateur" class="footer-link">⭐ GitHub</a>
        <a href="mailto:contact@exemple.com" class="footer-link">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
