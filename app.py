"""
Codex Validateur XML/JSON
Outil de validation et correction assistée pour fichiers DayZ
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from pathlib import Path

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="CodeX – Validateur XML / JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.block-container {
    background-color: #ffffff;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.main-title { font-size: 2.4em; font-weight: 700; color: #2d3748; }
.subtitle { color: #718096; margin-bottom: 10px; }

.dayz-tag {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 20px;
    border-radius: 20px;
    font-weight: 600;
}

.separator {
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 2px;
    margin: 30px 0;
}

.success-box {
    background: linear-gradient(135deg, #84fab0, #8fd3f4);
    padding: 20px;
    border-radius: 15px;
}

.error-box {
    background: linear-gradient(135deg, #fa709a, #fee140);
    padding: 20px;
    border-radius: 15px;
}

.step {
    font-weight: 600;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #718096;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE INIT
# ==============================
defaults = {
    "content": "",
    "filename": "",
    "filetype": None,
    "validated": False,
    "result_message": "",
    "result_ok": False,
    "formatted": "",
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# ==============================
# UTILS
# ==============================
def explain_xml_error(error):
    return f"""
Erreur de syntaxe XML détectée.

📍 Ligne {error.lineno}, colonne {error.offset}  
💬 {error.msg}

👉 Vérifie :
- les balises ouvertes / fermées
- les caractères spéciaux non échappés (&, <, >)
- la structure globale du fichier
"""

def explain_json_error(error):
    return f"""
Erreur de syntaxe JSON détectée.

📍 Ligne {error.lineno}, colonne {error.colno}  
💬 {error.msg}

👉 Vérifie :
- les guillemets doubles obligatoires
- les virgules en trop
- la structure des accolades et crochets
"""

def validate_xml(content):
    try:
        ET.fromstring(content)
        pretty = minidom.parseString(content).toprettyxml(indent="  ")
        return True, "✅ XML valide", pretty
    except ET.ParseError as e:
        return False, explain_xml_error(e), ""

def validate_json(content):
    try:
        data = json.loads(content)
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        return True, "✅ JSON valide", pretty
    except json.JSONDecodeError as e:
        return False, explain_json_error(e), ""

def auto_correct(content):
    corrected = content.replace("'", '"')
    corrected = re.sub(r',\s*([}\]])', r'\1', corrected)
    corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
    return corrected

# ==============================
# MAIN
# ==============================
def main():

    # BANNIÈRE
    try:
        st.image("images/codex3-V2.png", use_container_width=True)
    except:
        pass

    st.markdown('<h1 class="main-title">CodeX – Validateur XML / JSON</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Validation, compréhension et correction assistée de fichiers DayZ</p><div class="dayz-tag">🎮 Communauté DayZ Francophone</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # ==========================
    # ÉTAPE 1 – UPLOAD
    # ==========================
    st.markdown('<div class="step">1️⃣ Dépose ton fichier</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Formats acceptés : XML / JSON",
        type=["xml", "json"],
        disabled=bool(st.session_state.filename)
    )

    if uploaded:
        st.session_state.content = uploaded.read().decode("utf-8")
        st.session_state.filename = uploaded.name
        st.session_state.filetype = Path(uploaded.name).suffix.replace(".", "")
        st.session_state.validated = False

    if st.session_state.filename:
        st.info(f"📄 Fichier détecté : **{st.session_state.filename}**")

    # ==========================
    # ÉTAPE 2 – VALIDATION
    # ==========================
    if st.session_state.filename:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="step">2️⃣ Lance la validation</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        if st.session_state.filetype == "xml":
            if col1.button("🟢 Valider XML"):
                ok, msg, formatted = validate_xml(st.session_state.content)
                st.session_state.result_ok = ok
                st.session_state.result_message = msg
                st.session_state.formatted = formatted
                st.session_state.validated = True

        if st.session_state.filetype == "json":
            if col2.button("🔵 Valider JSON"):
                ok, msg, formatted = validate_json(st.session_state.content)
                st.session_state.result_ok = ok
                st.session_state.result_message = msg
                st.session_state.formatted = formatted
                st.session_state.validated = True

    # ==========================
    # ÉTAPE 3 – RÉSULTAT
    # ==========================
    if st.session_state.validated:
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="step">3️⃣ Résultat & aperçu</div>', unsafe_allow_html=True)

        if st.session_state.result_ok:
            st.markdown(f'<div class="success-box">{st.session_state.result_message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">{st.session_state.result_message}</div>', unsafe_allow_html=True)

        st.code(
            st.session_state.formatted if st.session_state.formatted else st.session_state.content,
            language=st.session_state.filetype
        )

        # ======================
        # ÉTAPE 4 – ACTIONS
        # ======================
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="step">4️⃣ Actions</div>', unsafe_allow_html=True)

        colA, colB, colC = st.columns(3)

        if colA.button("🔧 Corriger automatiquement"):
            st.session_state.content = auto_correct(st.session_state.content)
            st.session_state.validated = False
            st.success("Correction appliquée. Relance la validation.")

        colB.download_button(
            "⬇️ Télécharger le fichier",
            data=st.session_state.content,
            file_name=f"corrige_{st.session_state.filename}",
            mime="text/plain"
        )

        if colC.button("🗑️ Réinitialiser"):
            st.session_state.clear()
            st.rerun()

    # FOOTER
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">CodeX – Par EpSy ❤️ | Outil communautaire DayZ FR</div>', unsafe_allow_html=True)

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
