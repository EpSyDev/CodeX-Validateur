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

.block {
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 16px;
}

.identification { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.localisation { background: linear-gradient(135deg, #f6d365, #fda085); }
.description { background: linear-gradient(135deg, #fa709a, #fee140); }
.solution { background: linear-gradient(135deg, #84fab0, #8fd3f4); }

.codebox textarea {
    font-family: monospace !important;
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
defaults = {
    "content": "",
    "filename": "",
    "filetype": None,
    "error_info": None,
    "highlighted": "",
    "corrected": ""
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
            "type": "JSON",
            "line": err.lineno,
            "column": err.colno,
            "message": err.msg
        }
    elif isinstance(err, ET.ParseError):
        return {
            "type": "XML",
            "line": err.position[0],
            "column": err.position[1],
            "message": str(err)
        }
    return None

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
uploaded = st.file_uploader(
    "📤 Dépose ton fichier XML ou JSON",
    type=["xml", "json"],
    disabled=bool(st.session_state.filename)
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1]

# ==============================
# ACTION BUTTONS
# ==============================
if st.session_state.filename:
    st.info(
        f"📄 Fichier détecté : **{st.session_state.filename}**  \n"
        f"👉 Clique sur le bouton correspondant pour lancer la vérification."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🟢 Valider XML", disabled=st.session_state.filetype != "xml"):
            err = validate_xml(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error(
                    st.session_state.content, err["line"]
                )
            else:
                st.success("✅ Fichier XML valide")

    with col2:
        if st.button("🔵 Valider JSON", disabled=st.session_state.filetype != "json"):
            err = validate_json(st.session_state.content)
            if err:
                st.session_state.error_info = err
                st.session_state.highlighted = highlight_error(
                    st.session_state.content, err["line"]
                )
            else:
                st.success("✅ Fichier JSON valide")

# ==============================
# PEDAGOGICAL RESULT
# ==============================
if st.session_state.error_info:
    e = st.session_state.error_info

    st.markdown(f"""
<div class="block identification">
<h4>🧩 Identification</h4>
Type de fichier concerné : <b>{e["type"]}</b>
</div>

<div class="block localisation">
<h4>📍 Localisation</h4>
Ligne <b>{e["line"]}</b> — Colonne <b>{e["column"]}</b>
</div>

<div class="block description">
<h4>🧠 Description de l’erreur</h4>
{e["message"]}
</div>

<div class="block solution">
<h4>💡 Solution proposée</h4>
<ul>
<li>Vérifie l’ouverture et la fermeture des balises</li>
<li>Supprime les virgules finales (JSON)</li>
<li>Corrige les caractères spéciaux non échappés</li>
<li>Respecte strictement la structure attendue par DayZ</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.text_area(
        "🔍 Code analysé (zone défilante)",
        value=st.session_state.highlighted,
        height=350
    )

# ==============================
# CORRECTION
# ==============================
if st.session_state.error_info:
    if st.button("🔧 Corriger automatiquement"):
        st.session_state.corrected = auto_correct(st.session_state.content)
        st.session_state.content = st.session_state.corrected
        st.session_state.highlighted = st.session_state.corrected
        st.session_state.error_info = None
        st.success("✅ Correction appliquée — pense à revérifier le fichier")

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
    st.info("ℹ️ Le fichier devra être renommé exactement comme l’original pour DayZ")

# ==============================
# RESET
# ==============================
if st.button("🗑️ Réinitialiser l’analyse"):
    st.session_state.clear()
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown(
    '<div class="footer">Codex Validateur – EpSy ❤️ | DayZ FR</div>',
    unsafe_allow_html=True
)
