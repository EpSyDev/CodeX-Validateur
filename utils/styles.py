"""
Codex Suite - Styles centralisés
Import dans chaque page : from utils.styles import apply_styles
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

/* ── BASE ── */
* { font-family: 'Inter', sans-serif; }
.stApp { background: #000000; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── TEXTES FORCÉS EN BLANC (fix Opera/Edge mode sombre) ── */
p, li, span, label,
.stMarkdown,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] span,
div[data-testid="stCaptionContainer"],
.stCaption,
.stCheckbox label,
.stMultiSelect label,
.stSelectbox label,
.stRadio label,
.stTextInput label,
.stNumberInput label,
.stSlider label,
.stFileUploader label,
.stExpander label,
.streamlit-expanderContent p,
.streamlit-expanderContent li,
[data-testid="stWidgetLabel"] p
{ color: rgba(255, 255, 255, 0.85) !important; }

/* Titres */
h1, h2 { color: #FFFFFF !important; }
h3, h4  { color: #00D4FF !important; }

/* Tags multiselect → texte noir sur badge coloré */
.stMultiSelect div[data-baseweb="tag"] span { color: #000000 !important; }

/* Placeholder inputs */
input::placeholder,
textarea::placeholder { color: rgba(255,255,255,0.4) !important; }

/* ── BLOCS CODE documentation ── */
.stCode, 
[data-testid="stCode"],
pre, code {
    background: #1a1a2e !important;
    color: #00D4FF !important;
    border: 1px solid rgba(0, 212, 255, 0.2) !important;
    border-radius: 8px !important;
}

/* Texte dans les blocs code → lisible */
pre *, code * {
    color: #e0e0e0 !important;
}

/* Syntax highlighting conservé */
.stCode code {
    color: #e0e0e0 !important;
}

/* ── HEADER ── */
.header-container {
    width: 100%;
    margin: 0 0 40px 0;
    padding: 0;
}
.header-container img {
    width: 100%;
    height: auto;
    display: block;
}

/* ── LAYOUT ── */
.content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px 80px 30px;
}

.page-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 40px;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

/* ── COMPOSANTS CODEX ── */
.stats-box {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    color: white;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    margin: 6px 0;
}
.stats-box h2 { color: #00D4FF !important; margin: 0; font-size: 2em; }
.stats-box p  { margin: 4px 0 0 0; font-size: 0.85em; color: rgba(255,255,255,0.6) !important; }

.zone-card {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-left: 4px solid #00D4FF;
    color: rgba(255,255,255,0.85);
    padding: 15px 20px;
    border-radius: 16px;
    margin: 10px 0;
}
.zone-card h4 { color: #00D4FF !important; margin: 0 0 8px 0; font-size: 16px; font-weight: 700; }
.zone-card p  { margin: 4px 0; font-size: 0.9em; color: rgba(255,255,255,0.85) !important; }

.info-box {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 30px;
}
.info-box h3 { color: #00D4FF !important; font-size: 18px; font-weight: 700; margin-bottom: 12px; }
.info-box p  { color: rgba(255, 255, 255, 0.85) !important; font-size: 14px; line-height: 1.6; margin: 0; }

.calibration-note {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-left: 4px solid #00D4FF;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 8px;
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.9em;
}

.tip-box {
    background: rgba(0, 25, 50, 0.55);
    border-left: 3px solid #fbbf24;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.85em;
    color: rgba(255,255,255,0.8) !important;
    margin: 8px 0;
}

.pedagogy-box {
    background: rgba(0, 100, 150, 0.15);
    border-left: 4px solid #00D4FF;
    padding: 24px;
    margin: 20px 0;
    border-radius: 8px;
}
.pedagogy-box h3 { color: #00D4FF !important; margin: 0 0 20px 0; font-size: 20px; font-weight: 700; }

.result-box {
    background: rgba(0, 25, 50, 0.55);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
}
.result-box.success { border-color: rgba(0, 212, 255, 0.6); background: rgba(0, 50, 75, 0.4); }
.result-box.error   { border-color: rgba(239, 68, 68, 0.6);  background: rgba(75, 0, 0, 0.4); }

.error-item {
    background: rgba(239, 68, 68, 0.1);
    border-left: 3px solid #ef4444;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255,255,255,0.9) !important;
}
.warning-item {
    background: rgba(251, 191, 36, 0.1);
    border-left: 3px solid #fbbf24;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255,255,255,0.9) !important;
}

.correction-box {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%);
    border: 2px solid rgba(34, 197, 94, 0.4);
    border-radius: 16px;
    padding: 28px;
    margin: 24px 0;
}
.correction-box h3 { color: #22c55e !important; margin: 0 0 16px 0; font-size: 22px; font-weight: 800; }

.correction-badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #22c55e !important;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px 4px 12px 0;
}

.context-code {
    background: rgba(0, 0, 0, 0.6);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.6;
}
.context-code .line       { color: rgba(255,255,255,0.6) !important; padding: 2px 0; }
.context-code .line.error { background: rgba(239,68,68,0.2); border-left: 3px solid #ef4444; padding-left: 12px; color: #fff !important; }
.context-code .line-num   { display: inline-block; width: 40px; color: rgba(255,255,255,0.4) !important; text-align: right; margin-right: 16px; }

/* ── BOUTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000 !important;
    border: none;
    border-radius: 14px;
    padding: 16px 32px;
    font-size: 15px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 5px 18px rgba(0, 212, 255, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0, 15, 30, 0.8);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(0, 212, 255, 0.2);
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.6) !important;
    font-weight: 600;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 212, 255, 0.15) !important;
    color: #00D4FF !important;
}

/* ── RADIO ── */
.stRadio > div { gap: 12px; }
.stRadio label {
    background: rgba(0, 25, 50, 0.5);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    padding: 8px 16px;
    color: rgba(255,255,255,0.8) !important;
    transition: all 0.2s;
}
.stRadio label:has(input:checked) {
    background: rgba(0, 212, 255, 0.15);
    border-color: #00D4FF;
    color: #00D4FF !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(0, 25, 50, 0.6) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    color: white !important;
    border-radius: 8px;
}
.stTextArea textarea {
    background: rgba(0, 25, 50, 0.6) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    color: white !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(0, 25, 50, 0.6) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {
    color: rgba(255, 255, 255, 0.7) !important;
}
[data-testid="stFileDropzoneInstructions"] {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* ── SELECTBOX / MULTISELECT ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(0, 25, 50, 0.6) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    color: white !important;
}

/* ── TOGGLE ── */
.stToggle label { color: rgba(255,255,255,0.85) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%) !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
}

/* ── SIDEBAR (si utilisée) ── */
[data-testid="stSidebar"] { background: #0a0a1a !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
</style>
"""


def apply_styles(st):
    """Applique le CSS global CodeX. Appeler en début de chaque page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


HEADER_HTML = """
<div class="header-container">
    <img src="https://raw.githubusercontent.com/EpSyDev/codex-validateur/main/assets/images/codex_header.png" alt="CODEX">
</div>
"""


def apply_header(st):
    """Affiche le header CodeX. Appeler après apply_styles()."""
    st.markdown(HEADER_HTML, unsafe_allow_html=True)
