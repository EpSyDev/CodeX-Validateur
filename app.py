"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
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

.codebox textarea {
    max-height: 380px;
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
for key, default in {
    "content": "",
    "filename": "",
    "filetype": None,
    "error_info": None,
    "highlighted": "",
    "corrected": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ==============================
# UTILS
# ==============================
def highlight_error(content, line):
    lines = content.splitlines()
    if 1 <= line <= len(lines):
        lines[line - 1] = "🔴 ERREUR ICI → " + lines[line - 1]
    return "\n".join(lines)

def extract_error_info(err):
    if isinstance(err, json.JSONDecodeError):
        return {
            "type": "json",
            "line": err.lineno,
            "column": err.colno,
            "raw": err.msg
        }
    elif isinstance(err, ET.ParseError):
        return {
            "type": "xml",
            "line": err.position[0],
            "column": err.position[1],
            "raw": str(err)
        }
    return None

def explain_error(err):
    raw = err["raw"].lower()

    if err["type"] == "json":
        if "expecting ',' delimiter" in raw:
            return (
                "Erreur de syntaxe JSON",
                "Une virgule est manquante ou mal placée.",
                "Ajoute ou corrige la virgule entre deux éléments."
            )
        if "unterminated string" in raw:
            return (
                "Chaîne de caractères non fermée",
                "Un guillemet est manquant.",
                "Ajoute le guillemet fermant (\")."
            )
        return (
            "Structure JSON invalide",
            "Le fichier ne respecte pas la syntaxe JSON.",
            "Vérifie accolades, crochets et virgules."
        )

    if err["type"] == "xml":
        if "mismatched tag" in raw:
            return (
                "Balise XML incorrecte",
                "Une balise fermante ne correspond pas à l’ouvrante.",
                "Vérifie l’ouverture et la fermeture des balises."
            )
        return (
            "Structure XML invalide",
            "Le XML n’est pas bien formé.",
            "Vérifie l’imbrication et les caractères spéciaux."
        )

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
    st.session_state.filetype = uploaded.name.split(".")[-1].lower()

# ==============================
# VALIDATION
# ==============================
if st.session_state.filename:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🟩 Valider XML") and st.session_state.filetype == "xml":
            err = validate_xml(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error(
                    st.session_state.content, err["line"]
                )

    with col2:
        if st.button("🟦 Valider JSON") and st.session_state.filetype == "json":
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
    title, desc, solution = explain_error(e)

    st.markdown(f"""
<div class="error">
<h4>❌ {title}</h4>
<b>📍 Localisation :</b> Ligne {e["line"]}, Colonne {e["column"]}<br>
<b>🧠 Description :</b> {desc}
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="solution">
<h4>💡 Solution</h4>
{solution}
</div>
""", unsafe_allow_html=True)

    st.text_area(
        "🔍 Code analysé",
        value=st.session_state.highlighted,
        height=380,
        key="codebox"
    )

# ==============================
# CORRECTION
# ==============================
if st.session_state.error_info:
    if st.button("🔧 Corriger automatiquement"):
        st.session_state.content = auto_correct(st.session_state.content)
        st.session_state.error_info = None
        st.session_state.highlighted = st.session_state.content
        st.success("✅ Correction appliquée")

# ==============================
# DOWNLOAD
# ==============================
if st.session_state.content:
    st.download_button(
        "⬇️ Télécharger le fichier corrigé",
        data=st.session_state.content,
        file_name=st.session_state.filename,
        mime="text/plain"
    )
    st.info("ℹ️ Pense à renommer le fichier avec son nom d’origine si nécessaire")

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
