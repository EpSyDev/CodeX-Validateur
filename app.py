"""
Codex Validateur XML/JSON
L'outil indispensable pour vérifier vos fichiers de configuration DayZ
Créé par EpSy pour la communauté francophone DayZ
VERSION ULTIME - Images cliquables + Surlignage erreurs + Correction en place
"""

import streamlit as st
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Codex Validateur XML/JSON",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS personnalisé (optimisé pour images cliquables + surlignage)
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Style global */
    * { font-family: 'Inter', sans-serif; }
    
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
    .block-container { background-color: #ffffff; border-radius: 20px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    
    /* Header */
    .main-title { color: #2d3748; font-size: 2.5em; font-weight: 700; margin: 10px 0; }
    .subtitle { color: #718096; font-size: 1.1em; font-weight: 400; margin-bottom: 10px; }
    .dayz-tag { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 20px; border-radius: 20px; font-size: 0.9em; font-weight: 600; margin-top: 10px; }
    
    /* 🎯 BOUTONS IMAGES CLICABLES (correction finale) */
    .stButton > button {
        width: 100%; border: none; border-radius: 12px; padding: 0; height: 100px;
        background: transparent; transition: transform 0.2s, box-shadow 0.2s; cursor: pointer;
        position: relative; overflow: hidden;
    }
    .stButton > button:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.25); }
    .stButton > button:active { transform: translateY(-2px); }
    
    /* L'image remplit tout le bouton */
    .stButton > button img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
    
    /* Cache le texte vide du bouton */
    .stButton > button div[data-testid="stMarkdownContainer"] { display: none !important; }
    
    /* Zone de texte */
    .stTextArea textarea { border-radius: 12px; border: 2px solid #e2e8f0; font-family: 'Consolas', monospace; font-size: 14px; }
    .stTextArea textarea:focus { border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
    
    /* Messages */
    .success-box { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 5px 15px rgba(132, 250, 176, 0.3); }
    .success-title { color: #065f46; font-size: 1.5em; font-weight: 700; margin-bottom: 10px; }
    .success-text { color: #047857; font-size: 1.1em; line-height: 1.6; }
    
    .error-box { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 25px; border-radius: 15px; margin: 20px 0; box-shadow: 0 5px 15px rgba(250, 112, 154, 0.3); }
    .error-title { color: #7f1d1d; font-size: 1.5em; font-weight: 700; margin-bottom: 10px; }
    .error-text { color: #991b1b; font-size: 1.1em; line-height: 1.6; }
    
    .suggestion-box { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 20px; border-radius: 15px; margin: 15px 0; box-shadow: 0 5px 15px rgba(255, 236, 210, 0.3); }
    .suggestion-title { color: #92400e; font-size: 1.3em; font-weight: 700; margin-bottom: 10px; }
    .suggestion-item { color: #78350f; font-size: 1em; margin: 8px 0; padding-left: 20px; }
    
    /* Code avec surlignage erreur */
    .error-highlight { background-color: #fee140 !important; color: #991b1b !important; font-weight: bold; }
    
    /* Footer */
    .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #e2e8f0; color: #718096; }
    .discord-link { display: inline-block; background: #5865F2; color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 15px 0; transition: background 0.2s; }
    .discord-link:hover { background: #4752C4; }
    
    .separator { height: 3px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 2px; margin: 30px 0; }
    </style>
""", unsafe_allow_html=True)

# NOUVELLE FONCTION: Surligner la ligne d'erreur
def highlight_error_line(content, error=None, line_num=None):
    """Marque visuellement la ligne d'erreur dans le code"""
    lines = content.split('\n')
    
    if error and hasattr(error, 'lineno') and 1 <= error.lineno <= len(lines):
        line_num = error.lineno - 1
    elif line_num is not None:
        line_num -= 1
    
    if line_num is not None and 0 <= line_num < len(lines):
        lines[line_num] = f"🔴 ERREUR ICI: {lines[line_num]}"
    
    return '\n'.join(lines)

# Fonctions de validation (améliorées)
def validate_xml(content):
    results = {'valid': False, 'message': '', 'suggestions': [], 'formatted': '', 'highlighted': ''}
    try:
        root = ET.fromstring(content)
        pretty_xml = minidom.parseString(content).toprettyxml(indent="  ")
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        results.update({
            'valid': True,
            'message': "✅ Ton XML est parfait ! Toutes les balises sont OK.",
            'formatted': pretty_xml
        })
    except ET.ParseError as e:
        results.update({
            'valid': False,
            'message': f"❌ Erreur XML: {str(e)}",
            'suggestions': analyze_xml_error(content, str(e)),
            'highlighted': highlight_error_line(content, error=e)
        })
    return results

def analyze_xml_error(content, error):
    suggestions = []
    if 'mismatched tag' in error.lower():
        suggestions.extend(["🔴 Balise mal fermée", "💡 Vérifie <tag> et </tag>"])
    if 'not well-formed' in error.lower():
        suggestions.extend(["🔴 XML mal formé", "💡 Échappe & → &amp;"])
    return suggestions

def validate_json(content):
    results = {'valid': False, 'message': '', 'suggestions': [], 'formatted': '', 'highlighted': ''}
    try:
        data = json.loads(content)
        pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
        results.update({
            'valid': True,
            'message': "✅ Ton JSON est parfait ! Syntaxe impeccable.",
            'formatted': pretty_json
        })
    except json.JSONDecodeError as e:
        results.update({
            'valid': False,
            'message': f"❌ Erreur JSON ligne {e.lineno}: {str(e)}",
            'suggestions': analyze_json_error(content, e),
            'highlighted': highlight_error_line(content, error=e)
        })
    return results

def analyze_json_error(content, error):
    suggestions = [f"📍 Ligne {error.lineno}: {content.splitlines()[error.lineno-1][:100]}..."]
    error_msg = str(error).lower()
    if 'comma' in error_msg: suggestions.append("🔴 Virgule manquante ou en trop")
    if 'property name' in error_msg: suggestions.append("🔴 Clé sans guillemets: \"clé\": valeur")
    if 'brace' in error_msg or 'bracket' in error_msg: suggestions.append("🔴 Accolade/crochet non fermé")
    return suggestions

def auto_correct(content):
    corrected = content
    corrections = []
    
    # JSON: guillemets, virgules
    if content.strip().startswith(('{', '[')):
        corrected = corrected.replace("'", '"')
        corrected = re.sub(r',\s*([}\]])', r'\1', corrected)
        if "'" in content: corrections.append("guillemets simples → doubles")
        if re.search(r',\s*[}\]]', content): corrections.append("virgules en trop supprimées")
    
    # XML: échappement &
    corrected = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', corrected)
    if '&' in content: corrections.append("caractères & échappés")
    
    return corrected, corrections

# Interface principale
def main():
    if 'content' not in st.session_state: st.session_state.content = ''
    if 'uploaded_filename' not in st.session_state: st.session_state.uploaded_filename = 'fichier.txt'
    
    # Header
    try: st.image("images/codex3-V2.png", use_column_width=True)
    except: pass
    st.markdown('<h1 class="main-title">Codex Validateur XML/JSON</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pour tes configs DayZ</p><div class="dayz-tag">🎮 Communauté FR</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # 🎯 4 BOUTONS IMAGES CLICABLES
    st.markdown("### 🎯 Actions disponibles")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("XML", key="xml", help="Valider XML"): st.session_state.action = "xml"
        st.image("images/xml.png", use_column_width=True)
    
    with col2:
        if st.button("JSON", key="json", help="Valider JSON"): st.session_state.action = "json"
        st.image("images/json.png", use_column_width=True)
    
    with col3:
        if st.button("🔧", key="correct", help="Auto-corriger"): st.session_state.action = "correct"
        st.image("images/auto_corriger.png", use_column_width=True)
    
    with col4:
        if st.button("🗑️", key="clear", help="Effacer"): st.session_state.action = "clear"
        st.image("images/effacer.png", use_column_width=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Zone texte + upload (correction se fait EN PLACE)
    uploaded = st.file_uploader("📤 Glisse ton fichier", type=['xml','json','txt'])
    if uploaded:
        st.session_state.content = uploaded.read().decode('utf-8')
        st.session_state.uploaded_filename = uploaded.name
    
    st.session_state.content = st.text_area(
        "📝 Ton code ici:", value=st.session_state.content, height=350,
        placeholder="Colle ton XML ou JSON..."
    )
    
    # Actions
    if 'action' in st.session_state:
        action = st.session_state.action
        content = st.session_state.content
        
        if action == "clear":
            st.session_state = {'content': '', 'uploaded_filename': 'fichier.txt'}
            st.rerun()
        
        elif action == "correct" and content.strip():
            with st.spinner("🔧 Correction auto..."):
                corrected, corrs = auto_correct(content)
                if corrected != content:
                    st.session_state.content = corrected
                    st.markdown(f'<div class="success-box"><div class="success-title">✅ Corrigé !</div><div class="success-text">{", ".join(corrs)}</div></div>', unsafe_allow_html=True)
                    
                    # Download corrigé
                    ext = 'json' if corrected.startswith(('{','[')) else 'xml'
                    st.download_button("💾 Fichier corrigé", corrected, f"{Path(st.session_state.uploaded_filename).stem}_corrige.{ext}", 'text/plain')
                else:
                    st.info("ℹ️ Déjà parfait !")
        
        elif action in ("xml", "json"):
            if content.strip():
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
                results = validate_xml(content) if action == "xml" else validate_json(content)
                
                if results['valid']:
                    st.markdown(f'<div class="success-box"><div class="success-title">✅ Parfait !</div><div class="success-text">{results["message"]}</div></div>', unsafe_allow_html=True)
                    st.code(results['formatted'], language=action)
                    st.download_button("💾 Formaté", results['formatted'], f"fichier.{action}", mime=f'text/{action}')
                else:
                    st.markdown(f'<div class="error-box"><div class="error-title">❌ Erreur !</div><div class="error-text">{results["message"]}</div></div>', unsafe_allow_html=True)
                    
                    if results['suggestions']:
                        st.markdown('<div class="suggestion-box"><div class="suggestion-title">💡 Corrections:</div></div>', unsafe_allow_html=True)
                        for s in results['suggestions']: st.markdown(f'<div class="suggestion-item">• {s}</div>', unsafe_allow_html=True)
                    
                    # 🔴 SUR LIGNAGE DANS LE CODE
                    st.markdown("#### 📍 Code avec erreur marquée:")
                    st.code(results['highlighted'], language=action)
        
        del st.session_state.action
        st.rerun()
    
    # Footer
    st.markdown('<div class="separator"></div><div class="footer"><a href="https://discord.gg/CQR6KTJ63C" class="discord-link">💬 Discord FR</a><p>Par EpSy ❤️</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
