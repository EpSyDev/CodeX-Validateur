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
from modules.comparator import compare_before_after, compare_side_by_side
from modules.corrector import auto_correct, can_auto_correct, suggest_manual_fixes


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

.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 2px solid #e5e7eb;
    color: #6b7280;
}

.code-line-changed {
    background-color: #fef3c7;
    font-weight: 600;
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
    "validation_result": None,
    "corrected_content": None,
    "show_comparison": False,
    "user_level": "novice"  # novice ou modder
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
        index=0 if st.session_state.user_level == "novice" else 1,
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
    help="Fichiers DayZ acceptés : cfgweather.xml, cfgeventsapawns.xml, types.xml, cfggameplay.json, etc."
)

if uploaded:
    st.session_state.content = uploaded.read().decode("utf-8")
    st.session_state.filename = uploaded.name
    st.session_state.filetype = uploaded.name.split(".")[-1].lower()
    st.session_state.validation_result = None  # Reset validation si nouveau fichier
    st.session_state.corrected_content = None
    st.session_state.show_comparison = False


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
        st.session_state.corrected_content = None
        st.session_state.show_comparison = False

st.markdown("---")


# ==============================
# BOUTONS D'ACTION
# ==============================
if st.session_state.content:
    st.markdown("### 🎯 Actions disponibles")
    
    col_btn_1, col_btn_2, col_btn_3, col_btn_4 = st.columns(4)
    
    with col_btn_1:
        if st.button("🔍 Valider", use_container_width=True, type="primary"):
            with st.spinner("Validation en cours..."):
                result = validate(st.session_state.content, st.session_state.filetype)
                st.session_state.validation_result = result
                st.session_state.show_comparison = False
    
    with col_btn_2:
        # Bouton correction : actif uniquement si validation échouée
        can_correct = (
            st.session_state.validation_result and 
            not st.session_state.validation_result["valid"]
        )
        
        if st.button("🔧 Auto-corriger", use_container_width=True, disabled=not can_correct):
            with st.spinner("Correction en cours..."):
                correction = auto_correct(
                    st.session_state.content, 
                    st.session_state.filetype
                )
                
                if correction["has_changes"]:
                    st.session_state.corrected_content = correction["corrected"]
                    st.session_state.show_comparison = True
                    st.success(f"✅ {len(correction['applied_corrections'])} correction(s) appliquée(s)")
                else:
                    st.info("ℹ️ Aucune correction automatique possible pour cette erreur")
    
    with col_btn_3:
        if st.button("🗑️ Réinitialiser", use_container_width=True):
            for key in defaults.keys():
                st.session_state[key] = defaults[key]
            st.rerun()
    
    with col_btn_4:
        # Bouton téléchargement : toujours actif
        download_content = st.session_state.corrected_content or st.session_state.content
        st.download_button(
            "💾 Télécharger",
            data=download_content,
            file_name=st.session_state.filename,
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")


# ==============================
# AFFICHAGE DES RÉSULTATS
# ==============================
if st.session_state.validation_result:
    result = st.session_state.validation_result
    
    # ==============================
    # CAS 1 : FICHIER VALIDE
    # ==============================
    if result["valid"]:
        st.markdown("""
        <div class="success-block">
            <h3>✅ Nickel ! Ton fichier est parfait !</h3>
            <p>Aucune erreur détectée. Le fichier est prêt pour DayZ.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # ==============================
        # BLOC 1 : IDENTIFICATION
        # ==============================
        st.markdown(f"""
        <div class="block identification">
            <h4>🧩 Identification</h4>
            <p><strong>Type de fichier :</strong> {result["file_type"].upper()}</p>
            <p><strong>Erreur détectée :</strong> {matched["titre"] if matched else "Erreur de syntaxe"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 2 : LOCALISATION (avec smart locate pour XML)
        # ==============================
        reported_line = error["line"]
        real_line = reported_line
        confidence = None
        reason = None
        
        # Pour XML : utiliser locator pour trouver la vraie ligne
        if result["file_type"] == "xml":
            location = locate_real_error(st.session_state.content, reported_line)
            real_line = location["real_line"]
            confidence = location["confidence"]
            reason = location["reason"]
        
        # Affichage
        if result["file_type"] == "xml" and real_line != reported_line:
            # Cas où locator a trouvé une meilleure ligne
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation</h4>
                <p><strong>🎯 Ligne probable :</strong> {real_line} (confiance : {confidence})</p>
                <p><strong>Colonne :</strong> {error["column"]}</p>
                <p><strong>💡 Explication :</strong> {reason}</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    <em>Note : Le parseur indiquait ligne {reported_line}, mais l'analyse a identifié la cause réelle plus haut.</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Cas standard
            st.markdown(f"""
            <div class="block localisation">
                <h4>📍 Localisation</h4>
                <p><strong>Ligne :</strong> {real_line}</p>
                <p><strong>Colonne :</strong> {error["column"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 3 : DESCRIPTION
        # ==============================
        st.markdown(f"""
        <div class="block description">
            <h4>🧠 Description de l'erreur</h4>
            <p>{message_user}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 4 : SOLUTION
        # ==============================
        if matched:
            can_auto = can_auto_correct(matched)
            
            if can_auto:
                st.markdown(f"""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>✅ Cette erreur peut être corrigée automatiquement !</p>
                    <p>Clique sur le bouton <strong>"🔧 Auto-corriger"</strong> ci-dessus.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Suggestions manuelles
                suggestions = suggest_manual_fixes(
                    st.session_state.content,
                    result["file_type"],
                    matched
                )
                
                steps_html = "".join([f"<li>{step}</li>" for step in suggestions["manual_steps"]])
                
                st.markdown(f"""
                <div class="block solution">
                    <h4>💡 Solution</h4>
                    <p>⚠️ Cette erreur nécessite une correction manuelle.</p>
                    <p><strong>Étapes à suivre :</strong></p>
                    <ul>{steps_html}</ul>
                </div>
                """, unsafe_allow_html=True)
        
        # ==============================
        # BLOC 5 : CODE AVEC ERREUR
        # ==============================
        st.markdown("#### 📝 Code analysé")
        
        # Afficher le code avec numérotation des lignes
        lines = st.session_state.content.splitlines()
        
        # Marquer la ligne d'erreur
        highlighted_lines = []
        for i, line in enumerate(lines, start=1):
            if i == real_line:
                highlighted_lines.append(f"🔴 → {line}")
            else:
                highlighted_lines.append(f"     {line}")
        
        highlighted_code = "\n".join(highlighted_lines)
        
        st.code(highlighted_code, language=result["file_type"], line_numbers=True)
        
        # ==============================
        # BLOC 6 : EXEMPLE AVANT/APRÈS (si disponible)
        # ==============================
        if matched and matched.get("exemple_avant"):
            st.markdown("#### 📚 Exemple de correction")
            
            col_ex_1, col_ex_2 = st.columns(2)
            
            with col_ex_1:
                st.markdown("**❌ Avant (incorrect)**")
                st.code(matched["exemple_avant"], language=result["file_type"])
            
            with col_ex_2:
                st.markdown("**✅ Après (correct)**")
                st.code(matched["exemple_après"], language=result["file_type"])


# ==============================
# COMPARAISON AVANT/APRÈS (après correction auto)
# ==============================
if st.session_state.show_comparison and st.session_state.corrected_content:
    st.markdown("---")
    st.markdown("### 🔄 Comparaison avant / après correction")
    
    comparison = compare_side_by_side(
        st.session_state.content,
        st.session_state.corrected_content
    )
    
    col_comp_1, col_comp_2 = st.columns(2)
    
    with col_comp_1:
        st.markdown("**❌ Avant**")
        before_code = "\n".join([
            f"{'🔴 ' if changed else '   '}{content}"
            for num, content, changed in comparison["before_lines"]
        ])
        st.code(before_code, language=st.session_state.filetype, line_numbers=True)
    
    with col_comp_2:
        st.markdown("**✅ Après**")
        after_code = "\n".join([
            f"{'✅ ' if changed else '   '}{content}"
            for num, content, changed in comparison["after_lines"]
        ])
        st.code(after_code, language=st.session_state.filetype, line_numbers=True)
    
    # Bouton pour appliquer la correction
    col_apply_1, col_apply_2, col_apply_3 = st.columns([1, 1, 2])
    
    with col_apply_1:
        if st.button("✅ Appliquer la correction", use_container_width=True, type="primary"):
            st.session_state.content = st.session_state.corrected_content
            st.session_state.corrected_content = None
            st.session_state.validation_result = None
            st.session_state.show_comparison = False
            st.success("Correction appliquée ! Tu peux maintenant re-valider le fichier.")
            st.rerun()
    
    with col_apply_2:
        if st.button("❌ Annuler", use_container_width=True):
            st.session_state.corrected_content = None
            st.session_state.show_comparison = False
            st.rerun()


# ==============================
# FOOTER
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>Codex Validateur XML/JSON</strong></p>
        <p>Créé avec ❤️ par <strong>EpSy</strong> pour la communauté DayZ francophone</p>
        <p><a href="https://discord.gg/CQR6KTJ63C" target="_blank">💬 Rejoindre le Discord</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
