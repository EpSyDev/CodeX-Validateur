"""
Codex Validateur XML/JSON
L'outil indispensable pour vérifier vos fichiers de configuration DayZ
Créé par EpSy pour la communauté francophone DayZ
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

# Style CSS personnalisé
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Style global */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    
    .block-container {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Header avec logo */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .main-title {
        color: #2d3748;
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .subtitle {
        color: #718096;
        font-size: 1.1em;
        font-weight: 400;
        margin-bottom: 10px;
    }
    
    .dayz-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Boutons personnalisés */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 0;
        height: auto;
        background: transparent;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button img {
        width: 100%;
        height: auto;
        border-radius: 12px;
    }
    
    /* Zone de texte */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Messages de succès */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(132, 250, 176, 0.3);
    }
    
    .success-title {
        color: #065f46;
        font-size: 1.5em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .success-text {
        color: #047857;
        font-size: 1.1em;
        line-height: 1.6;
    }
    
    /* Messages d'erreur */
    .error-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(250, 112, 154, 0.3);
    }
    
    .error-title {
        color: #7f1d1d;
        font-size: 1.5em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .error-text {
        color: #991b1b;
        font-size: 1.1em;
        line-height: 1.6;
    }
    
    /* Suggestions */
    .suggestion-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(255, 236, 210, 0.3);
    }
    
    .suggestion-title {
        color: #92400e;
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .suggestion-item {
        color: #78350f;
        font-size: 1em;
        margin: 8px 0;
        padding-left: 20px;
    }
    
    /* Code formaté */
    .formatted-code {
        background-color: #1e293b;
        color: #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        overflow-x: auto;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 2px solid #e2e8f0;
        color: #718096;
    }
    
    .discord-link {
        display: inline-block;
        background: #5865F2;
        color: white;
        padding: 12px 30px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        margin: 15px 0;
        transition: background 0.2s;
    }
    
    .discord-link:hover {
        background: #4752C4;
    }
    
    .credit {
        font-size: 0.9em;
        color: #a0aec0;
        margin-top: 10px;
    }
    
    /* Séparateur stylé */
    .separator {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Fonctions de validation
def validate_xml(content):
    """Valide la syntaxe XML et retourne les résultats"""
    results = {
        'valid': False,
        'message': '',
        'suggestions': [],
        'formatted': ''
    }
    
    try:
        root = ET.fromstring(content)
        pretty_xml = minidom.parseString(content).toprettyxml(indent="  ")
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        results['valid'] = True
        results['message'] = f"Élément racine: <{root.tag}>\nNombre d'éléments enfants: {len(root)}"
        results['formatted'] = pretty_xml
        
    except ET.ParseError as e:
        results['valid'] = False
        results['message'] = str(e)
        results['suggestions'] = analyze_xml_error(content, str(e))
        
    return results

def analyze_xml_error(content, error_msg):
    """Analyse l'erreur XML et retourne des suggestions"""
    suggestions = []
    lines = content.split('\n')
    
    line_match = re.search(r'line (\d+)', error_msg)
    
    if line_match:
        error_line = int(line_match.group(1))
        suggestions.append(f"📍 L'erreur se trouve à la ligne {error_line}")
        
        if error_line <= len(lines):
            suggestions.append(f"Code concerné: {lines[error_line-1].strip()}")
    
    # Balises non fermées
    open_tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*>', content)
    close_tags = re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)>', content)
    
    open_count = {}
    for tag in open_tags:
        open_count[tag] = open_count.get(tag, 0) + 1
    
    for tag in close_tags:
        open_count[tag] = open_count.get(tag, 0) - 1
    
    unclosed = [tag for tag, count in open_count.items() if count > 0]
    if unclosed:
        suggestions.append(f"🔴 Balises non fermées détectées: {', '.join(unclosed)}")
        suggestions.append(f"💡 Ajoute les balises: {', '.join([f'</{tag}>' for tag in unclosed])}")
    
    # Caractères spéciaux
    if '&' in content and not any(esc in content for esc in ['&amp;', '&lt;', '&gt;', '&quot;', '&apos;']):
        suggestions.append("🔴 Caractère '&' non échappé détecté")
        suggestions.append("💡 Remplace '&' par '&amp;'")
    
    # Attributs sans guillemets
    if re.search(r'<[^>]*\s+\w+=\w+[^>]*>', content):
        suggestions.append("🔴 Attributs sans guillemets détectés")
        suggestions.append("💡 Mets les valeurs entre guillemets")
    
    if not suggestions:
        suggestions.append("🤔 Vérifie la structure générale de ton XML")
    
    return suggestions

def validate_json(content):
    """Valide la syntaxe JSON et retourne les résultats"""
    results = {
        'valid': False,
        'message': '',
        'suggestions': [],
        'formatted': ''
    }
    
    try:
        data = json.loads(content)
        pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
        
        results['valid'] = True
        if isinstance(data, dict):
            results['message'] = f"Type: Objet\nNombre de clés: {len(data)}"
        elif isinstance(data, list):
            results['message'] = f"Type: Tableau\nNombre d'éléments: {len(data)}"
        results['formatted'] = pretty_json
        
    except json.JSONDecodeError as e:
        results['valid'] = False
        results['message'] = f"Ligne: {e.lineno}, Colonne: {e.colno}\n{str(e)}"
        results['suggestions'] = analyze_json_error(content, e)
        
    return results

def analyze_json_error(content, error):
    """Analyse l'erreur JSON et retourne des suggestions"""
    suggestions = []
    lines = content.split('\n')
    
    if error.lineno <= len(lines):
        suggestions.append(f"📍 L'erreur se trouve à la ligne {error.lineno}")
        suggestions.append(f"Code concerné: {lines[error.lineno-1].strip()}")
    
    error_msg = str(error).lower()
    
    if 'expecting' in error_msg and ',' in error_msg:
        suggestions.append("🔴 Il manque une virgule entre les éléments")
        suggestions.append("💡 Ajoute une virgule après l'élément précédent")
    
    if 'expecting property name' in error_msg:
        suggestions.append("🔴 Les clés doivent être entre guillemets doubles")
        suggestions.append('💡 Utilise "clé": "valeur" et non clé: "valeur"')
    
    if 'trailing comma' in error_msg or 'expecting value' in error_msg:
        suggestions.append("🔴 Virgule en trop à la fin d'un objet ou tableau")
        suggestions.append("💡 Supprime la dernière virgule avant } ou ]")
    
    open_braces = content.count('{')
    close_braces = content.count('}')
    open_brackets = content.count('[')
    close_brackets = content.count(']')
    
    if open_braces != close_braces:
        diff = open_braces - close_braces
        if diff > 0:
            suggestions.append(f"🔴 {diff} accolade(s) '{{' non fermée(s)")
            suggestions.append(f"💡 Ajoute {diff} accolade(s) de fermeture '}}'")
        else:
            suggestions.append(f"🔴 {-diff} accolade(s) '}}' en trop")
    
    if open_brackets != close_brackets:
        diff = open_brackets - close_brackets
        if diff > 0:
            suggestions.append(f"🔴 {diff} crochet(s) '[' non fermé(s)")
            suggestions.append(f"💡 Ajoute {diff} crochet(s) de fermeture ']'")
        else:
            suggestions.append(f"🔴 {-diff} crochet(s) ']' en trop")
    
    if not suggestions:
        suggestions.append("🤔 Vérifie la structure générale de ton JSON")
    
    return suggestions

def auto_correct(content):
    """Tentative de correction automatique"""
    is_json = content.strip().startswith(('{', '['))
    corrected = content
    
    if is_json:
        corrected = corrected.replace("'", '"')
        corrected = re.sub(r',\s*}', '}', corrected)
        corrected = re.sub(r',\s*]', ']', corrected)
    else:
        corrected = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', corrected)
    
    return corrected

# Interface principale
def main():
    # Header avec logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("images/Codex3.png", width=200)
        except:
            pass
    
    st.markdown('<h1 class="main-title">Codex Validateur XML/JSON</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">L\'outil indispensable pour vérifier vos fichiers de configuration DayZ</p>', unsafe_allow_html=True)
    st.markdown('<div class="dayz-tag">🎮 Communauté DayZ Francophone</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Boutons d'action
    st.markdown("### 🎯 Actions disponibles")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        try:
            st.image("images/charger_fichier.png", width=200)
        except:
            pass
        if st.button("📁", key="load", help="Charger fichier"):
            st.session_state.action = "load"
    
    with col2:
        try:
            st.image("images/xml.png", width=200)
        except:
            pass
        if st.button("XML", key="xml", help="Valider XML"):
            st.session_state.action = "xml"
    
    with col3:
        try:
            st.image("images/json.png", width=200)
        except:
            pass
        if st.button("JSON", key="json", help="Valider JSON"):
            st.session_state.action = "json"
    
    with col4:
        try:
            st.image("images/auto_corriger.png", width=200)
        except:
            pass
        if st.button("🔧", key="correct", help="Auto-corriger"):
            st.session_state.action = "correct"
    
    with col5:
        try:
            st.image("images/effacer.png", width=200)
        except:
            pass
        if st.button("🗑️", key="clear", help="Effacer"):
            st.session_state.action = "clear"
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Zone de saisie
    if 'content' not in st.session_state:
        st.session_state.content = ""
    
    uploaded_file = st.file_uploader("📤 Ou glisse ton fichier ici", type=['xml', 'json', 'txt'])
    
    if uploaded_file is not None:
        st.session_state.content = uploaded_file.read().decode('utf-8')
    
    content = st.text_area(
        "📝 Colle ou édite ton code ici:",
        value=st.session_state.content,
        height=300,
        placeholder="Colle ton code XML ou JSON ici..."
    )
    
    st.session_state.content = content
    
    # Actions
    if 'action' in st.session_state:
        action = st.session_state.action
        
        if action == "clear":
            st.session_state.content = ""
            st.rerun()
        
        elif action == "correct":
            if content.strip():
                corrected = auto_correct(content)
                st.session_state.content = corrected
                st.success("✅ Corrections automatiques appliquées ! Vérifie le résultat ci-dessus.")
                st.rerun()
            else:
                st.warning("⚠️ Rien à corriger, ajoute du code d'abord !")
        
        elif action == "xml":
            if content.strip():
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
                st.markdown("### 📊 Résultats de validation XML")
                
                results = validate_xml(content)
                
                if results['valid']:
                    st.markdown(f"""
                        <div class="success-box">
                            <div class="success-title">✅ Nickel ! Ton XML est parfait !</div>
                            <div class="success-text">{results['message'].replace(chr(10), '<br>')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### 🎨 Code formaté:")
                    st.code(results['formatted'], language='xml')
                else:
                    st.markdown(f"""
                        <div class="error-box">
                            <div class="error-title">❌ Oups ! Y'a un souci dans ton XML</div>
                            <div class="error-text">{results['message'].replace(chr(10), '<br>')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if results['suggestions']:
                        st.markdown("""
                            <div class="suggestion-box">
                                <div class="suggestion-title">💡 Voici comment le corriger:</div>
                            </div>
                        """, unsafe_allow_html=True)
                        for suggestion in results['suggestions']:
                            st.markdown(f"<div class='suggestion-item'>• {suggestion}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Ajoute du code XML d'abord !")
        
        elif action == "json":
            if content.strip():
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
                st.markdown("### 📊 Résultats de validation JSON")
                
                results = validate_json(content)
                
                if results['valid']:
                    st.markdown(f"""
                        <div class="success-box">
                            <div class="success-title">✅ Nickel ! Ton JSON est parfait !</div>
                            <div class="success-text">{results['message'].replace(chr(10), '<br>')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### 🎨 Code formaté:")
                    st.code(results['formatted'], language='json')
                else:
                    st.markdown(f"""
                        <div class="error-box">
                            <div class="error-title">❌ Oups ! Y'a un souci dans ton JSON</div>
                            <div class="error-text">{results['message'].replace(chr(10), '<br>')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if results['suggestions']:
                        st.markdown("""
                            <div class="suggestion-box">
                                <div class="suggestion-title">💡 Voici comment le corriger:</div>
                            </div>
                        """, unsafe_allow_html=True)
                        for suggestion in results['suggestions']:
                            st.markdown(f"<div class='suggestion-item'>• {suggestion}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Ajoute du code JSON d'abord !")
        
        del st.session_state.action
    
    # Footer
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            <p style="font-size: 1.1em; color: #2d3748; font-weight: 600;">
                Rejoins notre communauté DayZ francophone ! 🎮
            </p>
            <a href="https://discord.gg/CQR6KTJ63C" target="_blank" class="discord-link">
                💬 Rejoindre le Discord
            </a>
            <p class="credit">
                Créé avec ❤️ par <strong>EpSy</strong> pour la communauté
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
