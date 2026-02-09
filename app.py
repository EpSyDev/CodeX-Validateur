"""
Codex Suite - Test minimal
"""

import streamlit as st

st.set_page_config(
    page_title="Codex Suite",
    page_icon="images/favicon.png",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #000000;
}

h1 {
    color: #00D4FF !important;
    text-align: center;
}

p {
    color: #38BDF8 !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# CODEX SUITE")
st.markdown("### La boîte à outils DayZ")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📝 Validateur")
    if st.button("Ouvrir", key="v"):
        st.switch_page("pages/1_Validateur.py")

with col2:
    st.markdown("### 🗺️ Carte")
    if st.button("Ouvrir", key="m"):
        st.switch_page("pages/2_Carte_Interactive.py")

with col3:
    st.markdown("### 📚 Documentation")
    if st.button("Ouvrir", key="d"):
        st.switch_page("pages/3_Documentation.py")
