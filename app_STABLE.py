"""
Codex Suite - Page d'accueil
Arctic Blue Edition - Version stable
"""

import streamlit as st

st.set_page_config(
    page_title="Codex Suite",
    page_icon="❄️",
    layout="wide"
)

# CSS simplifié et stable
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
}

h1, h2, h3 {
    color: #bae6fd !important;
}

p {
    color: #7dd3fc !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7);
    color: white;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 700;
    border: none;
}

.stButton > button:hover {
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# ❄️ CODEX SUITE")
st.markdown("### La boîte à outils ultime pour DayZ")

st.markdown("---")

# Modules
st.markdown("## 🚀 Modules disponibles")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📝 Validateur")
    st.markdown("Valide et corrige automatiquement tes fichiers de configuration DayZ")
    if st.button("Ouvrir le Validateur", key="val"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("### 🗺️ Carte Interactive")
    st.markdown("Édite visuellement les spawns zombies sur les cartes DayZ")
    if st.button("Ouvrir la Carte", key="map"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("### 📚 Documentation")
    st.markdown("Apprends à maîtriser les fichiers de configuration DayZ")
    if st.button("Ouvrir la Doc", key="doc"):
        st.switch_page("pages/3_Documentation.py")

st.markdown("---")

# Stats
st.markdown("## 📊 En chiffres")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Fichiers supportés", "5+")
s2.metric("Corrections auto", "100%")
s3.metric("Maps", "3")
s4.metric("Pages doc", "170+")

st.markdown("---")

# Footer
st.markdown("**CODEX SUITE v3.0**")
st.markdown("Créé avec ❤️ par **EpSy** pour la communauté DayZ francophone")
