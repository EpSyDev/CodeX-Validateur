"""
Codex Validateur XML/JSON
Outil pédagogique de validation et correction
Créé par EpSy – Communauté DayZ Francophone
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier modules au path Python
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from modules.validator import validate
from modules.locator import locate_real_error
from modules.corrector import suggest_manual_fixes


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
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.identification { 
    background: linear-gradient(135deg, #667eea, #764ba2); 
    color: white; 
}

.localisation { 
    background: linear-gradient(135deg, #f6d365, #fda085); 
    color: #7c2d12;
}

.description { 
    background: linear-gradient(135deg, #fa709a, #fee140); 
    color: #7f1d1d;
}

.solution { 
    background: linear-gradient(135deg, #84fab0, #8fd3f4); 
    color: #065f46;
}

.success-block {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
}

/* ✨ NOUVEAU : Bloc warnings sémantiques */
.semantic-warnings {
    background: linear-gradient(135deg, #fef3c7, #fbbf24);
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
    border: 2px solid #f59e0b;
}

.warning-item {
    background: white;
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #f59e0b;
}

.error-item {
    background: white;
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #dc2626;
}

/* ✨ NOUVEAU : Badge type fichier */
.dayz-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9em;
    margin-left: 10px;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 2px solid #e5e7eb;
    color: #6b7280;
}

/* Scroll pour le code analysé */
.code-scroll {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px;
    background: #f9fafb;
}

/* Comparaison après correction */
.correction-result {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    padding: 20px;
    border-radius: 14px;
    margin: 20px 0;
    border: 2px solid #10b981;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# ✨ NOUVEAU : SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("### 📚 Documentation")
    
    github_base = "https://github.com/nicolassmt/codex-validateur/blob/main/docs/"
    
    st.markdown(f"""
    **Fichiers DayZ documentés :**
    - 📄 [types.xml]({github_base}TYPES_XML_DOCUMENTATION.md)
    - 🚁 [events.xml]({github_base}EVENTS_XML_DOCUMENTATION.md)
    - 💰 [economy.xml]({github_base}ECONOMY_XML_DOCUMENTATION.md)
    - 🌐 [globals.xml]({github_base}GLOBALS_XML_DOCUMENTATION.md)
    - 💬 [messages.xml]({github_base}MESSAGES_XML_DOCUMENTATION.md)
    """)
    
    st.markdown("---")
    
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    **Codex Validateur** v2.0
    
    Validation syntaxique ET sémantique des fichiers DayZ.
    
    🔍 Détecte les erreurs  
    ✅ Corrige automatiquement  
    📚 Valide les règles métier
    """)
    
    st.markdown("---")
    
    st.markdown("### 💬 Communauté")
    st.markdown("[Discord](https://discord.gg/CQR6KTJ63C)")


# ==============================
# SESSION STATE
# ==============================
defaults = {
    "content": "",
    "filename": "",
    "filetype": None,
    "validation_result": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ==============================
# HEADER
# ==============================
try:
    st.image("images/codex3-V2.png", use_column_width=True)
except:
    pass

st.title("🎮 Codex Validateur XML / JSON")
st.subheader("Comprendre, corriger et fiabiliser tes fichiers DayZ")

# Sélecteur de niveau utilisateur
col_level_1, col_level_2, col_level_3 = st.columns([1, 1, 2])
with col_level_1:
    user_level = st.radio(
        "Ton niveau :",
        ["novice", "modder"],
        index=0 if st.session_state.get("user_level", "novice") == "novice" else 1,
        horizontal=True
    )
    st.session_state.user_level = user_level

st.markdown("---")


# ==============================
# UPLOAD
# ==============================
uploaded = st.file_uploader(
    "📤 Dépose ton fichier XML ou JSON",
    type=["xml", "json"],
    help="Fichiers DayZ acceptés : types.xml, events.xml, economy.xml, globals.xml, messages.xml, etc."
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1].lower()
    st.session_state.validation_result = None


# ==============================
# ZONE DE TEXTE (si pas de fichier uploadé)
# ==============================
if not uploaded:
    st.markdown("### ✏️ Ou colle ton code directement ici")
    
    col_type_1, col_type_2 = st.columns(2)
    with col_type_1:
        manual_type = st.selectbox(
            "Type de fichier",
            ["xml", "json"],
            help="Sélectionne le type de ton code"
        )
    
    content_input = st.text_area(
        "Code",
        value=st.session_state.content,
        height=300,
        placeholder="Colle ton code XML ou JSON ici..."
    )
    
    if content_input != st.session_state.content:
        st.session_state.content = content_input
        st.session_state.filetype = manual_type
        st.session_state.filename = f"code_colle.{manual_type}"
        st.session_state.validation_result = None

st.markdown("---")


# ==============================
# BOUTONS D'ACTION
# ==============================
if st.session_state.content:
    st.markdown("### 🎯 Actions disponibles")
    
    col_btn_1, col_btn_2, col_btn_3 = st.columns(3)
    
    with col_btn_1:
        if st.button("🔍 Valider", use_container_width=True, type="primary"):
            with st.spinner("Validation en cours..."):
                result = validate(st.session_state.content, st.session_state.filetype)
                st.session_state.validation_result = result
    
    with col_btn_2:
        if st.button("🗑️ Réinitialiser", use_container_width=True):
            for key in defaults.keys():
                st.session_state[key] = defaults[key]
            st.rerun()
    
    with col_btn_3:
        # Bouton télécharger actif si validation OK OU correction disponible
        download_enabled = False
        download_content = st.session_state.content
        download_filename = st.session_state.filename
        
        if st.session_state.validation_result:
            result = st.session_state.validation_result
            
            if result["valid"]:
                download_enabled = True
                download_content = result["formatted"]
            elif result.get("corrected"):
                download_enabled = True
                download_content = result["corrected"]
                # Renommer le fichier
                name_parts = st.session_state.filename.rsplit(".", 1)
                if len(name_parts) == 2:
                    download_filename = f"{name_parts[0]}_corrige.{name_parts[1]}"
                else:
                    download_filename = f"{st.session_state.filename}_corrige"
        
        if download_enabled:
            st.download_button(
                "💾 Télécharger",
                data=download_content,
                file_name=download_filename,
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("💾 Télécharger", use_container_width=True, disabled=True, help="Valide d'abord ton fichier")

st.markdown("---")


# ==============================
# AFFICHAGE DES RÉSULTATS
# ==============================
if st.session_state.validation_result:
    result = st.session_state.validation_result
    
    # ✨ NOUVEAU : Afficher le type DayZ détecté
    if result.get("dayz_type"):
        dayz_type_names = {
            "types": "types.xml (Items & Loot)",
            "events": "events.xml (Événements dynamiques)",
            "economy": "economy.xml (Économie globale)",
            "globals": "globals.xml (Variables serveur)",
            "messages": "messages.xml (Messages automatiques)"
        }
        dayz_display = dayz_type_names.get(result["dayz_type"], result["dayz_type"])
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <span class="dayz-badge">📄 Fichier détecté : {dayz_display}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # ==============================
    # CAS 1 : FICHIER VALIDE
    # ==============================
    if result["valid"]:
        st.markdown("""
        <div class="success-block">
            <h3>✅ Nickel ! Ton fichier est parfait syntaxiquement !</h3>
            <p>Aucune erreur de syntaxe détectée. Le fichier est prêt pour DayZ.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ✨ NOUVEAU : Afficher les warnings sémantiques si présents
        if result.get("semantic_warnings") and len(result["semantic_warnings"]) > 0:
            warnings = result["semantic_warnings"]
            errors_count = sum(1 for w in warnings if w["severity"] == "error")
            warnings_count = sum(1 for w in warnings if w["severity"] == "warning")
            
            st.markdown(f"""
            <div class="semantic-warnings">
                <h3>⚠️ Validation sémantique : {errors_count} erreur(s), {warnings_count} avertissement(s)</h3>
                <p>La syntaxe est correcte, mais certaines <strong>règles métier DayZ</strong> ne sont pas respectées :</p>
            </div>
            """, unsafe_allow_html=True)
            
            for warning in warnings:
                severity_icon = "🔴" if warning["severity"] == "error" else "⚠️"
                severity_class = "error-item" if warning["severity"] == "error" else "warning-item"
                severity_label = "ERREUR MÉTIER" if warning["severity"] == "error" else "AVERTISSEMENT"
                
                st.markdown(f"""
                <div class="{severity_class}">
                    <p><strong>{severity_icon} {severity_label}</strong></p>
                    <p>{warning["message"]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recommandations
            if errors_count > 0:
                st.warning("⚠️ **Action recommandée :** Corrige les erreurs métier ci-dessus avant d'utiliser ce fichier sur ton serveur. Ces erreurs peuvent causer des dysfonctionnements in-game.")
            else:
                st.info("💡 **Info :** Les avertissements ci-dessus sont des suggestions d'amélioration. Le fichier fonctionnera, mais ces ajustements sont recommandés.")
        
        st.markdown("#### 🎨 Code formaté")
        st.code(result["formatted"], language=result["file_type"], line_numbers=True)
    
    # ==============================
    # CAS 2 : FICHIER AVEC ERREUR
    # ==============================
    else:
        error = result["error"]
        matched = error["matched"]
        
        # Niveau de message selon utilisateur
        if matched:
            if st.session_state.user_level == "novice":
                message_user = matched["message_novice"]
            else:
                message_user = matched["message_modder"]
        else:
            message_user = error["message_brut"]
        
        # Calcul de la vraie ligne (smart locate pour XML)
        reported_line = error["line"]
        real_line = reported_line
        confidence = None
        reason = None
        
        if result["file_type"] == "xml":
            location = locate_real_error(st.session_state.content, reported_line)
            real_line = location["real_line"]
            confidence = location["confidence"]
            reason = location["reason"]
        
        # ==============================
        # AFFICHAGE CORRECTION AUTO (si disponible) EN PREMIER
        # ==============================
        if result.get("corrected"):
            st.markdown("""
            <div class="correction-result">
                <h3>✅ Correction automatique disponible !</h3>
                <p>L'erreur a été corrigée automatiquement. Compare l'extrait ci-dessous et télécharge le fichier complet.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔄 Comparaison avant / après (extrait autour de l'erreur)")
            
            # Extraire ±5 lignes autour de l'erreur
            lines_before = st.session_state.content.splitlines()
            lines_after = result["corrected"].splitlines()
            
            start_line = max(1, real_line - 5)
            end_line = min(len(lines_before), real_line + 5)
            
            col_comp_1, col_comp_2 = st.columns(2)
            
            with col_comp_1:
                st.markdown("**❌ Avant**")
                before_extract = []
                for i in range(start_line, end_line + 1):
                    if i <= len(lines_before):
                        line_content = lines_before[i - 1]
                        if i == real_line:
                            before_extract.append(f"🔴 {line_content}")
                        else:
                            before_extract.append(f"   {line_content}")
                
                st.code("\n".join(before_extract), language=result["file_type"], line_numbers=True)
            
            with col_comp_2:
                st.markdown("**✅ Après**")
                after_extract = []
                for i in range(start_line, end_line + 1):
                    if i <= len(lines_after):
                        line_content = lines_after[i - 1]
                        if i == real_line:
                            after_extract.append(f"✅ {line_content}")
                        else:
                            after_extract.append(f"   {line_content}")
                
                st.code("\n".join(after_extract), language=result["file_type"], line_numbers=True)
            
            st.markdown("---")
        
        # ==============================
        # BLOC 1 : LOCALISATION
        # ==============================
        if result["file_type"] == "xml" and real_line != reported_line:
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation de l'erreur</h4>
                <p><b>🎯 Ligne probable :</b> {real_line} (confiance : {confidence})</p>
                <p><b>Colonne :</b> {error["column"]}</p>
                <p><b>💡 Explication :</b> {reason}</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    <em>Note : Le parseur indiquait ligne {reported_line}, mais l'analyse a identifié la cause réelle plus haut.</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation de l'erreur</h4>
                <p><b>Ligne :</b> {real_line}</p>
                <p><b>Colonne :</b> {error["column"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 2 : EXTRAIT RÉEL
        # ==============================
        st.markdown("#### 📝 Extrait autour de l'erreur")
        
        lines = st.session_state.content.splitlines()
        start_line = max(1, real_line - 3)
        end_line = min(len(lines), real_line + 3)
        
        extract_lines = []
        for i in range(start_line, end_line + 1):
            line_content = lines[i - 1] if i <= len(lines) else ""
            if i == real_line:
                extract_lines.append(f"🔴 LIGNE {i} → {line_content}")
            else:
                extract_lines.append(f"   LIGNE {i}   {line_content}")
        
        extract_code = "\n".join(extract_lines)
        st.code(extract_code, language=result["file_type"])
        
        # ==============================
        # BLOC 3 : IDENTIFICATION
        # ==============================
        st.markdown(f"""
        <div class="block identification">
            <h4>🧩 Identification</h4>
            <p><b>Type de fichier :</b> {result["file_type"].upper()}</p>
            <p><b>Erreur détectée :</b> {matched["titre"] if matched else "Erreur de syntaxe"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 4 : DESCRIPTION
        # ==============================
        st.markdown(f"""
        <div class="block description">
            <h4>🧠 Description de l'erreur</h4>
            <p>{message_user}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 5 : SOLUTION
        # ==============================
        if matched:
            if result.get("corrected"):
                # Correction auto déjà disponible
                st.markdown("""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>✅ <strong>Cette erreur a été corrigée automatiquement !</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**👉 Action immédiate :**")
                st.markdown("""
                1. Vérifie la comparaison avant/après ci-dessus
                2. Télécharge le fichier complet corrigé avec **"💾 Télécharger"**
                3. Utilise le fichier téléchargé dans DayZ
                """)
            else:
                # Correction manuelle nécessaire
                suggestions = suggest_manual_fixes(
                    st.session_state.content,
                    result["file_type"],
                    matched
                )
                
                st.markdown("""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>⚠️ <strong>Cette erreur nécessite une correction manuelle.</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**👉 Étapes à suivre :**")
                manual_steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(suggestions["manual_steps"])])
                st.markdown(f"""
                {manual_steps}
                {len(suggestions["manual_steps"]) + 1}. Modifie ton fichier selon ces indications
                {len(suggestions["manual_steps"]) + 2}. Re-charge le fichier corrigé dans l'outil
                {len(suggestions["manual_steps"]) + 3}. Clique sur **"🔍 Valider"** pour vérifier
                """)
        
        # ==============================
        # BLOC 6 : CODE COMPLET (avec scroll)
        # ==============================
        st.markdown("#### 📄 Code complet analysé")
        
        highlighted_lines = []
        for i, line in enumerate(lines, start=1):
            if i == real_line:
                highlighted_lines.append(f"🔴 → {line}")
            else:
                highlighted_lines.append(f"     {line}")
        
        highlighted_code = "\n".join(highlighted_lines)
        
        st.markdown('<div class="code-scroll">', unsafe_allow_html=True)
        st.code(highlighted_code, language=result["file_type"], line_numbers=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Exemple de la DB en expander
        if matched and matched.get("exemple_avant"):
            with st.expander("💡 Voir un exemple de correction similaire"):
                col_ex_1, col_ex_2 = st.columns(2)
                
                with col_ex_1:
                    st.markdown("**❌ Avant (incorrect)**")
                    st.code(matched["exemple_avant"], language=result["file_type"])
                
                with col_ex_2:
                    st.markdown("**✅ Après (correct)**")
                    st.code(matched["exemple_après"], language=result["file_type"])


# ==============================
# FOOTER
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>Codex Validateur XML/JSON</strong> v2.0</p>
        <p>Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
        <p><a href="https://discord.gg/CQR6KTJ63C" target="_blank">💬 Rejoindre le Discord</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
