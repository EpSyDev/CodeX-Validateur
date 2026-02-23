"""
Codex Suite - Documentation
Guide complet des fichiers de configuration DayZ
"""

import streamlit as st
from pathlib import Path

# ═══════════════════════════════════════════════════════
# CONFIG PAGE
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="Codex - Documentation",
    page_icon="images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# CSS UNIFIÉ
# ═══════════════════════════════════════════════════════

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import apply_styles, apply_header

apply_styles(st)
apply_header(st)

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
st.markdown('<h1 class="page-title">📚 Documentation DayZ</h1>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <h3>🎯 Guide Complet</h3>
    <p>Apprenez à maîtriser tous les fichiers de configuration DayZ. Chaque section contient des explications détaillées, des exemples et des bonnes pratiques.</p>
</div>
""", unsafe_allow_html=True)

# Onglets par catégorie
tab1, tab2, tab3 = st.tabs(["📄 Fichiers XML", "📋 Fichiers JSON", "🔧 Bonnes Pratiques"])

with tab1:
    st.markdown("### Fichiers XML")
    
    # types.xml
    st.markdown("""
    <div class="doc-card">
        <h4>📝 types.xml</h4>
        <p><strong>Rôle :</strong> Définit tous les objets du jeu et leurs propriétés de spawn</p>
        <p><strong>Structure principale :</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
<types>
    <type name="AKM">
        <nominal>5</nominal>
        <lifetime>3600</lifetime>
        <restock>1800</restock>
        <min>3</min>
        <quantmin>-1</quantmin>
        <quantmax>-1</quantmax>
        <cost>100</cost>
        <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
        <category name="weapons"/>
        <usage name="Military"/>
        <value name="Tier3"/>
    </type>
</types>
    """, language="xml")
    
    st.markdown("""
    **Paramètres clés :**
    - `nominal` : Nombre d'objets visés sur la map
    - `lifetime` : Durée de vie en secondes
    - `restock` : Délai avant respawn
    - `min` : Nombre minimum garanti
    """)
    
    # events.xml
    st.markdown("""
    <div class="doc-card">
        <h4>🎯 events.xml</h4>
        <p><strong>Rôle :</strong> Gère les événements dynamiques (hélicos crash, convois...)</p>
        <p><strong>Structure principale :</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
<events>
    <event name="StaticHeliCrash">
        <nominal>3</nominal>
        <min>3</min>
        <max>5</max>
        <lifetime>2400</lifetime>
        <restock>0</restock>
        <saferadius>500</saferadius>
        <distanceradius>500</distanceradius>
        <cleanupradius>100</cleanupradius>
        <flags deletable="0" init_random="0" remove_damaged="1"/>
        <position>fixed</position>
        <limit>mixed</limit>
        <active>1</active>
        <children>
            <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_UH1Y"/>
        </children>
    </event>
</events>
    """, language="xml")
    
    # globals.xml
    st.markdown("""
    <div class="doc-card">
        <h4>🌍 globals.xml</h4>
        <p><strong>Rôle :</strong> Paramètres globaux de l'économie du serveur</p>
        <p><strong>Variables importantes :</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
<variables>
    <var name="TimeLogin" type="0" value="15"/>
    <var name="TimePenalty" type="0" value="20"/>
    <var name="TimeLogout" type="0" value="15"/>
    <var name="FlagRefreshFrequency" type="0" value="432000"/>
    <var name="FlagRefreshMaxDuration" type="0" value="3456000"/>
</variables>
    """, language="xml")

with tab2:
    st.markdown("### Fichiers JSON")
    
    # cfggameplay.json
    st.markdown("""
    <div class="doc-card">
        <h4>🎮 cfggameplay.json</h4>
        <p><strong>Rôle :</strong> Configuration du gameplay (santé, stamina, environnement)</p>
        <p><strong>Sections principales :</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
{
    "GeneralData": {
        "disableBaseDamage": 0,
        "disableContainerDamage": 0,
        "disableRespawnDialog": 0
    },
    "PlayerData": {
        "ShockRefillSpeedConscious": 5.0,
        "ShockRefillSpeedUnconscious": 1.0,
        "HealthRegenSpeed": 5.0
    },
    "StaminaData": {
        "StaminaMax": 100.0,
        "StaminaDepletionSpeed": 1.0,
        "StaminaRecoverySpeed": 5.0
    }
}
    """, language="json")
    
    # cfgeffectarea.json
    st.markdown("""
    <div class="doc-card">
        <h4>☣️ cfgeffectarea.json</h4>
        <p><strong>Rôle :</strong> Zones contaminées et zones dynamiques</p>
        <p><strong>Structure :</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
{
    "ContaminatedArea": {
        "Enabled": 1,
        "PositionVar": [3707.97, 2364.62],
        "Radius": 150.0,
        "NegHeight": 50.0,
        "PosHeight": 150.0
    }
}
    """, language="json")

with tab3:
    st.markdown("### 🔧 Bonnes Pratiques")
    
    st.markdown("""
    <div class="doc-card">
        <h4>✅ Validation Avant Déploiement</h4>
        <p>Toujours valider vos fichiers avant de les uploader sur le serveur :</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. ✅ **Utilisez le validateur Codex** pour détecter les erreurs
    2. ✅ **Faites une backup** avant toute modification
    3. ✅ **Testez sur serveur de test** avant production
    4. ✅ **Documentez vos changements** pour traçabilité
    """)
    
    st.markdown("""
    <div class="doc-card">
        <h4>⚡ Optimisation Performance</h4>
        <p>Conseils pour un serveur fluide :</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - 🎯 **Limitez les nominal** : Trop d'objets = lag
    - ⏱️ **Ajustez les lifetime** : Évitez l'accumulation
    - 📍 **Optimisez les events** : Maximum 3-5 événements simultanés
    - 🧹 **Nettoyage régulier** : Configurez les cleanup radius
    """)
    
    st.markdown("""
    <div class="doc-card">
        <h4>🔒 Sécurité</h4>
        <p>Protégez votre configuration :</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - 🔐 **Permissions fichiers** : Lecture seule après validation
    - 💾 **Backups automatiques** : Script quotidien recommandé
    - 📝 **Versioning** : Git pour tracker les modifications
    - 🚨 **Alertes** : Surveillance des erreurs serveur
    """)

st.markdown('</div>', unsafe_allow_html=True)
