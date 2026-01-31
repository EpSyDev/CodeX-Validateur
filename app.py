"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

# ==============================
# CONFIG PAGE
# ==============================
st.set_page_config(
    page_title="Codex Validateur XML/JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
* { font-family: Inter, sans-serif; }

.error {
    background: linear-gradient(135deg, #fa709a, #fee140);
    padding: 20px;
    border-radius: 14px;
}

.solution {
    background: linear-gradient(135deg, #84fab0, #8fd3f4);
    padding: 20px;
    border-radius: 14px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #718096;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
if "content" not in st.session_state:
    st.session_state.content = ""
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "filetype" not in st.session_state:
    st.session_state.filetype = None
if "error_info" not in st.session_state:
    st.session_state.error_info = None
if "highlighted" not in st.session_state:
    st.session_state.highlighted = ""
if "corrected" not in st.session_state:
    st.session_state.corrected = ""

# ==============================
# UTILS
# ==============================
def highlight_error(content, line):
    lines = content.splitlines()
    if 1 <= line <= len(lines):
        lines[line - 1] = "🔴 ERREUR ICI → " + lines[line - 1]
    return "\n".join(lines)

def extract_error_info(err):
    """Normalise XML / JSON errors"""
    if isinstance(err, json.JSONDecodeError):
        return {
            "line": err.lineno,
            "column": err.colno,
            "message": err.msg
        }
    elif isinstance(err, ET.ParseError):
        return {
            "line": err.position[0],
            "column": err.position[1],
            "message": str(err)
        }
    else:
        return {
            "line": "?",
            "column": "?",
            "message": str(err)
        }

def validate_json(content):
    try:
        json.loads(content)
        return None
    except json.JSONDecodeError as e:
        return extract_error_info(e)

def validate_xml(content):
    try:
        ET.fromstring(content)
        return None
    except ET.ParseError as e:
        return extract_error_info(e)

def auto_correct(content):
    corrected = re.sub(r',\s*([}\]])', r'\1', content)
    corrected = corrected.replace("'", '"')
    corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
    return corrected

# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🎮 Codex Validateur XML / JSON")
st.subheader("Comprendre, corriger et fiabiliser tes fichiers DayZ")

# ==============================
# UPLOAD
# ==============================
uploaded = st.file_uploader("📤 Dépose ton fichier XML ou JSON", type=["xml", "json"])

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1]

# ==============================
# VALIDATION
# ==============================
if st.session_state.filename:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Valider XML") and st.session_state.filetype == "xml":
            err = validate_xml(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error(
                    st.session_state.content, err["line"]
                )

    with col2:
        if st.button("Valider JSON") and st.session_state.filetype == "json":
            err = validate_json(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error(
                    st.session_state.content, err["line"]
                )

# ==============================
# RÉSULTAT
# ==============================
if st.session_state.error_info:
    e = st.session_state.error_info

    st.markdown(f"""
<div class="error">
<h4>❌ Erreur détectée</h4>
<b>📍 Localisation :</b> Ligne {e["line"]}, Colonne {e["column"]}<br>
<b>🧠 Description :</b> {e["message"]}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="solution">
<h4>💡 Solution</h4>
<ul>
<li>Vérifie la ligne indiquée</li>
<li>Supprime les virgules finales</li>
<li>Vérifie les caractères spéciaux (&, <, >)</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.text_area(
        "🔍 Code concerné",
        value=st.session_state.highlighted,
        height=380
    )

# ==============================
# CORRECTION
# ==============================
if st.session_state.error_info:
    if st.button("🔧 Corriger automatiquement"):
        st.session_state.corrected = auto_correct(st.session_state.content)
        st.session_state.content = st.session_state.corrected
        st.session_state.error_info = None
        st.session_state.highlighted = ""
        st.success("✅ Correction appliquée")

# ==============================
# DOWNLOAD
# ==============================
if st.session_state.corrected:
    st.download_button(
        "⬇️ Télécharger le fichier corrigé",
        data=st.session_state.corrected,
        file_name=st.session_state.filename,
        mime="text/plain"
    )
    st.info("ℹ️ Pense à renommer le fichier comme l’original si nécessaire")

# ==============================
# RESET
# ==============================
if st.button("🗑️ Réinitialiser"):
    st.session_state.clear()
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown('<div class="footer">Codex Validateur – EpSy ❤️ | DayZ FR</div>', unsafe_allow_html=True)
