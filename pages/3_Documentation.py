"""
Codex Suite - Documentation
Guide complet des fichiers de configuration DayZ
Charge les fichiers .md depuis docs/
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import apply_styles, apply_header

# ═══════════════════════════════════════════════════════
# CONFIG PAGE
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Codex - Documentation",
    page_icon="assets/images/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_styles(st)
apply_header(st)

# ═══════════════════════════════════════════════════════
# HELPER
# ═══════════════════════════════════════════════════════
def load_doc(filename):
    path = Path(__file__).parent.parent / "docs" / filename
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return f"⚠️ Documentation `{filename}` introuvable dans `docs/`."

# ═══════════════════════════════════════════════════════
# HEADER + NAV
# ═══════════════════════════════════════════════════════
if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("app.py")

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">📚 Documentation DayZ</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h3>🎯 Guide Complet</h3>
    <p>Maîtrisez tous les fichiers de configuration DayZ. Chaque section contient une description rapide du rôle du fichier, sa structure et un accès à la documentation complète.</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📄 Fichiers XML", "📋 Fichiers JSON", "🔧 Bonnes Pratiques"])

# ───────────────────────────────────────────────────────
# TAB 1 — FICHIERS XML
# ───────────────────────────────────────────────────────
with tab1:
    st.markdown("### Fichiers XML")

    # ── types.xml ──
    st.markdown("""
    <div class="doc-card">
        <h4>📝 types.xml</h4>
        <p><strong>Rôle :</strong> Définit tous les objets du jeu et leurs propriétés de spawn — loot, véhicules, équipements. C'est le fichier central de l'économie DayZ.</p>
        <p><strong>Impact :</strong> Nominal, lifetime, restock, catégories, tiers de zones.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""<types>
    <type name="AKM">
        <nominal>5</nominal>
        <lifetime>3600</lifetime>
        <restock>1800</restock>
        <min>3</min>
        <flags count_in_cargo="0" count_in_map="1" crafted="0" deloot="0"/>
        <category name="weapons"/>
        <usage name="Military"/>
        <value name="Tier3"/>
    </type>
</types>""", language="xml")

    with st.expander("📖 Documentation complète — types.xml"):
        st.markdown(load_doc("TYPES_XML_DOCUMENTATION.md"))

    st.markdown("---")

    # ── events.xml ──
    st.markdown("""
    <div class="doc-card">
        <h4>🎯 events.xml</h4>
        <p><strong>Rôle :</strong> Gère les événements dynamiques du serveur — crashs d'hélicos, convois militaires, zones contaminées, animaux.</p>
        <p><strong>Impact :</strong> Fréquence d'apparition, durée de vie, radius de nettoyage.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""<events>
    <event name="StaticHeliCrash">
        <nominal>3</nominal>
        <min>3</min>
        <max>5</max>
        <lifetime>2400</lifetime>
        <restock>0</restock>
        <saferadius>500</saferadius>
        <cleanupradius>100</cleanupradius>
        <flags deletable="0" init_random="0" remove_damaged="1"/>
        <position>fixed</position>
        <active>1</active>
        <children>
            <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_UH1Y"/>
        </children>
    </event>
</events>""", language="xml")

    with st.expander("📖 Documentation complète — events.xml"):
        st.markdown(load_doc("EVENTS_XML_DOCUMENTATION.md"))

    st.markdown("---")

    # ── economy.xml ──
    st.markdown("""
    <div class="doc-card">
        <h4>💰 economy.xml</h4>
        <p><strong>Rôle :</strong> Contrôle le système d'économie centrale — persistence des objets, véhicules, bases joueurs et zombies.</p>
        <p><strong>Impact :</strong> Ce fichier est critique — une mauvaise config peut faire disparaître bases et véhicules.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 Documentation complète — economy.xml"):
        st.markdown(load_doc("ECONOMY_XML_DOCUMENTATION.md"))

    st.markdown("---")

    # ── globals.xml ──
    st.markdown("""
    <div class="doc-card">
        <h4>🌍 globals.xml</h4>
        <p><strong>Rôle :</strong> 31 variables globales du serveur — limites de zombies et animaux, timers de cleanup, durabilité du loot, refresh des bases.</p>
        <p><strong>Impact :</strong> Paramètres globaux affectant l'ensemble du comportement serveur.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""<variables>
    <var name="TimeLogin" type="0" value="15"/>
    <var name="TimePenalty" type="0" value="20"/>
    <var name="TimeLogout" type="0" value="15"/>
    <var name="FlagRefreshFrequency" type="0" value="432000"/>
    <var name="FlagRefreshMaxDuration" type="0" value="3456000"/>
</variables>""", language="xml")

    with st.expander("📖 Documentation complète — globals.xml"):
        st.markdown(load_doc("GLOBALS_XML_DOCUMENTATION.md"))

    st.markdown("---")

    # ── messages.xml ──
    st.markdown("""
    <div class="doc-card">
        <h4>💬 messages.xml</h4>
        <p><strong>Rôle :</strong> Messages automatiques serveur — bienvenue, annonces périodiques, restarts programmés avec compte à rebours.</p>
        <p><strong>Impact :</strong> Communication directe avec les joueurs en jeu. Hot-reload possible.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""<messages>
    <message>
        <onconnect>1</onconnect>
        <text>👋 Bienvenue sur #name !</text>
    </message>
    <message>
        <repeat>30</repeat>
        <text>💬 Discord : discord.gg/VOTRECODE</text>
    </message>
    <message>
        <deadline>1440</deadline>
        <shutdown>1</shutdown>
        <text>⚠️ #name redémarrera dans #tmin minutes</text>
    </message>
</messages>""", language="xml")

    with st.expander("📖 Documentation complète — messages.xml"):
        st.markdown(load_doc("MESSAGES_XML_DOCUMENTATION.md"))

# ───────────────────────────────────────────────────────
# TAB 2 — FICHIERS JSON
# ───────────────────────────────────────────────────────
with tab2:
    st.markdown("### Fichiers JSON")

    # ── cfggameplay.json ──
    st.markdown("""
    <div class="doc-card">
        <h4>🎮 cfggameplay.json</h4>
        <p><strong>Rôle :</strong> Configuration du gameplay — santé, stamina, environnement, comportements joueurs.</p>
        <p><strong>Impact :</strong> Expérience de jeu directe, équilibre survie/combat.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""{
    "GeneralData": {
        "disableBaseDamage": 0,
        "disableContainerDamage": 0,
        "disableRespawnDialog": 0
    },
    "PlayerData": {
        "ShockRefillSpeedConscious": 5.0,
        "HealthRegenSpeed": 5.0
    },
    "StaminaData": {
        "StaminaMax": 100.0,
        "StaminaDepletionSpeed": 1.0,
        "StaminaRecoverySpeed": 5.0
    }
}""", language="json")

    st.markdown("---")

    # ── cfgeffectarea.json ──
    st.markdown("""
    <div class="doc-card">
        <h4>☣️ cfgeffectarea.json</h4>
        <p><strong>Rôle :</strong> Définit les zones contaminées statiques et dynamiques — position, rayon, hauteur d'effet.</p>
        <p><strong>Impact :</strong> Zones NBC, effets visuels et de contamination en jeu.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""{
    "ContaminatedArea": {
        "Enabled": 1,
        "PositionVar": [3707.97, 2364.62],
        "Radius": 150.0,
        "NegHeight": 50.0,
        "PosHeight": 150.0
    }
}""", language="json")

    st.markdown("---")

    # ── cfgweather.json ──
    st.markdown("""
    <div class="doc-card">
        <h4>🌦️ cfgweather.json</h4>
        <p><strong>Rôle :</strong> Configuration de la météo dynamique — pluie, brouillard, vent, overcast. Paramètres min/max et vitesse de transition.</p>
        <p><strong>Impact :</strong> Atmosphère et difficulté de survie (hypothermie, visibilité).</p>
    </div>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────────────
# TAB 3 — BONNES PRATIQUES
# ───────────────────────────────────────────────────────
with tab3:
    st.markdown("### 🔧 Bonnes Pratiques")

    st.markdown("""
    <div class="doc-card">
        <h4>✅ Validation Avant Déploiement</h4>
        <p>Toujours valider vos fichiers avant de les uploader sur le serveur.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
1. ✅ **Utilisez le Validateur Codex** pour détecter les erreurs XML/JSON
2. ✅ **Faites une backup** avant toute modification
3. ✅ **Testez sur serveur de test** avant la production
4. ✅ **Documentez vos changements** pour la traçabilité
    """)

    st.markdown("""
    <div class="doc-card">
        <h4>⚡ Optimisation Performance</h4>
        <p>Conseils pour un serveur fluide et stable.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
- 🎯 **Limitez les nominal** — Trop d'objets = lag serveur
- ⏱️ **Ajustez les lifetime** — Évitez l'accumulation d'objets
- 📍 **Optimisez les events** — 3 à 5 événements simultanés max
- 🧹 **Nettoyage régulier** — Configurez les cleanup radius correctement
- 🐺 **Animaux et zombies** — Limitez via globals.xml selon les perfs
    """)

    st.markdown("""
    <div class="doc-card">
        <h4>🔒 Sécurité & Versioning</h4>
        <p>Protégez votre configuration et gardez un historique.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
- 💾 **Backups automatiques** — Script quotidien recommandé
- 📝 **Git** — Tracker toutes les modifications avec des commits clairs
- 🚨 **Surveillance** — Monitorer les erreurs serveur au lancement
- 🔐 **Permissions** — Fichiers en lecture seule après validation en prod
    """)

    st.markdown("""
    <div class="doc-card">
        <h4>📋 Ordre de Modification Recommandé</h4>
        <p>Pour un admin débutant, voici la progression logique.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
1. **globals.xml** — Variables simples, impact direct et visible
2. **types.xml** — Ajuster le loot progressivement, tester à chaque étape
3. **events.xml** — Fréquence des événements dynamiques
4. **economy.xml** — ⚠️ Fichier critique, toucher en dernier
5. **messages.xml** — Communication joueurs, hot-reload possible
    """)

st.markdown('</div>', unsafe_allow_html=True)
