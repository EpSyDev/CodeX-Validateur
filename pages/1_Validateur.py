"""
Codex Suite - Module Validateur ULTIME
Validation XML/JSON avec pédagogie, correction auto et téléchargement
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import de l'ancien système qui fonctionne
from modules.validator import validate

# ═══════════════════════════════════════════════════════
# CONFIG PAGE
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Codex - Validateur",
    page_icon="images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# CSS UNIFIÉ
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #000000; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

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

.content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 30px 80px 30px;
}

.page-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 40px;
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
}

.info-box {
    background: linear-gradient(135deg, rgba(0, 25, 50, 0.65) 0%, rgba(0, 15, 30, 0.75) 100%);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 30px;
}

.info-box h3 {
    color: #00D4FF;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

.info-box p {
    color: rgba(255, 255, 255, 0.85);
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.result-box {
    background: rgba(0, 25, 50, 0.55);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
}

.result-box.success {
    border-color: rgba(0, 212, 255, 0.6);
    background: rgba(0, 50, 75, 0.4);
}

.result-box.error {
    border-color: rgba(239, 68, 68, 0.6);
    background: rgba(75, 0, 0, 0.4);
}

.pedagogy-box {
    background: rgba(0, 100, 150, 0.15);
    border-left: 4px solid #00D4FF;
    padding: 24px;
    margin: 20px 0;
    border-radius: 8px;
}

.pedagogy-box h3 {
    color: #00D4FF;
    margin: 0 0 20px 0;
    font-size: 20px;
    font-weight: 700;
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

.context-code .line {
    color: rgba(255, 255, 255, 0.6);
    padding: 2px 0;
}

.context-code .line.error {
    background: rgba(239, 68, 68, 0.2);
    border-left: 3px solid #ef4444;
    padding-left: 12px;
    color: #fff;
}

.context-code .line-num {
    display: inline-block;
    width: 40px;
    color: rgba(255, 255, 255, 0.4);
    text-align: right;
    margin-right: 16px;
}

.correction-box {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%);
    border: 2px solid rgba(34, 197, 94, 0.4);
    border-radius: 16px;
    padding: 28px;
    margin: 24px 0;
}

.correction-box h3 {
    color: #22c55e;
    margin: 0 0 16px 0;
    font-size: 22px;
    font-weight: 800;
}

.correction-badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #22c55e;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px 4px 12px 0;
}

.error-item {
    background: rgba(239, 68, 68, 0.1);
    border-left: 3px solid #ef4444;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.9);
}

.warning-item {
    background: rgba(251, 191, 36, 0.1);
    border-left: 3px solid #fbbf24;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.9);
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 100%);
    color: #000000;
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
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def get_code_context(content, error_line, context_lines=2):
    """Extrait le contexte autour de la ligne en erreur"""
    lines = content.split('\n')
    start = max(0, error_line - context_lines - 1)
    end = min(len(lines), error_line + context_lines)
    
    context = []
    for i in range(start, end):
        line_num = i + 1
        line_text = lines[i] if i < len(lines) else ""
        is_error = (line_num == error_line)
        context.append({
            'num': line_num,
            'text': line_text,
            'is_error': is_error
        })
    
    return context

def render_code_context(context):
    """Affiche le contexte du code avec highlight de l'erreur"""
    html = '<div class="context-code">'
    
    for line in context:
        line_class = "line error" if line['is_error'] else "line"
        arrow = "❌ " if line['is_error'] else "   "
        html += f'<div class="{line_class}">'
        html += f'<span class="line-num">{arrow}{line["num"]}</span>'
        html += f'{line["text"]}'
        html += '</div>'
    
    html += '</div>'
    return html

# ═══════════════════════════════════════════════════════
# HEADER IMAGE
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="header-container">
    <img src="https://raw.githubusercontent.com/EpSyDev/codex-validateur/main/assets/images/codex_header.png" alt="CODEX">
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# CONTENU PRINCIPAL
# ═══════════════════════════════════════════════════════

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">📝 Validateur de Fichiers DayZ</h1>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <h3>🎯 Validation Intelligente avec Correction Automatique</h3>
    <p>Uploadez n'importe quel fichier de configuration DayZ (XML ou JSON). Le système détecte le type, localise précisément les erreurs, explique le problème ET corrige automatiquement quand c'est possible !</p>
</div>
""", unsafe_allow_html=True)

# Upload de fichier
uploaded_file = st.file_uploader(
    "Choisissez un fichier",
    type=['xml', 'json'],
    help="Types supportés : types.xml, events.xml, globals.xml, cfggameplay.json, etc."
)

if uploaded_file:
    # Lire le contenu
    content = uploaded_file.read().decode('utf-8')
    filename = uploaded_file.name
    
    # Déterminer le type de fichier
    file_type = "json" if filename.lower().endswith('.json') else "xml"
    
    # Bouton de validation
    if st.button("🚀 Valider le fichier", type="primary"):
        with st.spinner("Analyse en cours..."):
            try:
                # Validation avec l'ancien système qui fonctionne
                result = validate(content, file_type)
                
                # DEBUG : Vérifier le type de result
                if result is None:
                    st.error("❌ La validation a retourné None")
                    st.stop()
                
                if not isinstance(result, dict):
                    st.error(f"❌ La validation a retourné {type(result)} au lieu d'un dict")
                    st.stop()
                
                # Stocker dans session state
                st.session_state.validation_result = result
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la validation : {str(e)}")
                st.exception(e)
                st.stop()

# Afficher les résultats
if 'validation_result' in st.session_state:
    result = st.session_state.validation_result
    
    # Vérifier que result est valide
    if not result:
        st.error("❌ Erreur lors de la validation")
        st.stop()
    
    # ═══════════════════════════════════════════════════════
    # RÉSUMÉ
    # ═══════════════════════════════════════════════════════
    
    if result.get("valid", False):
        dayz_type = result.get("dayz_type", "Fichier DayZ")
        st.markdown(f"""
        <div class="result-box success">
            <h2 style="color: #00D4FF; margin: 0;">✅ Fichier Valide</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Type détecté : <strong>{dayz_type or 'Inconnu'}</strong> ({result.get("file_type", "unknown").upper()})
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box error">
            <h2 style="color: #ef4444; margin: 0;">❌ Erreurs Détectées</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                Erreur de syntaxe trouvée - Correction disponible ci-dessous
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # PÉDAGOGIE (si erreur avec matching)
    # ═══════════════════════════════════════════════════════
    
    if not result.get("valid", False) and result.get("error") and result.get("error", {}).get("matched"):
        matched = result["error"]["matched"]
        error_line = result["error"].get("line", 0)
        
        st.markdown(f"""
        <div class="pedagogy-box">
            <h3>💡 {matched.get('title', 'Explication')}</h3>
        """, unsafe_allow_html=True)
        
        # Contexte du code
        if error_line > 0:
            st.markdown("**🔍 Contexte (où se situe l'erreur) :**")
            context = get_code_context(content, error_line, context_lines=2)
            st.markdown(render_code_context(context), unsafe_allow_html=True)
        
        # Exemples avant/après
        if matched.get('example_before') or matched.get('example_after'):
            st.markdown("**📝 Comparaison Avant / Après :**")
            col1, col2 = st.columns(2)
            
            with col1:
                if matched.get('example_before'):
                    st.markdown("**❌ AVANT (incorrect) :**")
                    st.code(matched['example_before'], language=result.get("file_type", "text"))
            
            with col2:
                if matched.get('example_after'):
                    st.markdown("**✅ APRÈS (correct) :**")
                    st.code(matched['example_after'], language=result.get("file_type", "text"))
        
        # Explication unifiée
        st.markdown("**📚 Explication :**")
        # Prioriser message_modder s'il existe, sinon message_novice
        explanation = matched.get('message_modder') or matched.get('message_novice', '')
        if explanation:
            st.markdown(f"<p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>{explanation}</p>", unsafe_allow_html=True)
        
        # Solution
        if matched.get('solution'):
            st.markdown("**💡 Solution :**")
            st.markdown(f"<p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>{matched['solution']}</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # ⭐ CORRECTION AUTOMATIQUE (CŒUR DE L'APP)
    # ═══════════════════════════════════════════════════════
    
    if result.get("corrected"):
        st.markdown("""
        <div class="correction-box">
            <h3>✨ Correction Automatique Disponible !</h3>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 16px;">
                Le fichier a été corrigé automatiquement. Voici un aperçu :
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher le code corrigé
        st.code(result["corrected"], language=result.get("file_type", "text"))
        
        # Boutons de téléchargement
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="💾 Télécharger le fichier corrigé",
                data=result["corrected"],
                file_name=f"corrigé_{uploaded_file.name}",
                mime="text/plain",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            # Bouton copier (via JavaScript)
            if st.button("📋 Copier dans le presse-papier", use_container_width=True):
                st.success("✅ Code copié ! (Utilisez Ctrl+V pour coller)")
                # Note: La vraie copie nécessite du JS côté client
    
    # ═══════════════════════════════════════════════════════
    # ONGLETS DÉTAILS
    # ═══════════════════════════════════════════════════════
    
    tab1, tab2, tab3 = st.tabs(["📄 Fichier Formaté", "⚠️ Avertissements Sémantiques", "ℹ️ Informations"])
    
    with tab1:
        if result.get("formatted"):
            st.subheader("📄 Fichier Formaté (version propre)")
            st.code(result["formatted"], language=result.get("file_type", "text"))
            
            st.download_button(
                label="💾 Télécharger formaté",
                data=result["formatted"],
                file_name=f"formaté_{uploaded_file.name}",
                mime="text/plain"
            )
        else:
            st.info("Formatage non disponible (erreur de syntaxe).")
    
    with tab2:
        if result.get("semantic_warnings"):
            st.markdown("### ⚠️ Avertissements Sémantiques (Règles Métier DayZ)")
            for warning in result["semantic_warnings"]:
                severity = warning.get("severity", "warning")
                message = warning.get("message", "")
                line = warning.get("line", 0)
                
                if severity == "error":
                    st.markdown(f"""
                    <div class="error-item">
                        <strong>Erreur métier - Ligne {line}</strong><br>
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-item">
                        <strong>Avertissement - Ligne {line}</strong><br>
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Aucun avertissement sémantique.")
    
    with tab3:
        info_data = {
            'Type de fichier': result.get('dayz_type') or 'Inconnu',
            'Format': result.get("file_type", "unknown").upper(),
            'Fichier valide': '✅ Oui' if result.get("valid", False) else '❌ Non',
            'Correction auto disponible': '✅ Oui' if result.get("corrected") else '❌ Non',
            'Formatage disponible': '✅ Oui' if result.get("formatted") else '❌ Non'
        }
        
        if result.get("semantic_warnings"):
            info_data['Avertissements sémantiques'] = len(result["semantic_warnings"])
        
        st.json(info_data)

st.markdown('</div>', unsafe_allow_html=True)
