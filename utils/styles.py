import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import io
import sys
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CodeX — Comparateur",
    page_icon="images/favicon.png",
    layout="wide",
)

# ─────────────────────────────────────────────
#  STYLE UNIFIÉ + HEADER
# ─────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import apply_styles, apply_header
apply_styles(st)
apply_header(st)

# ─────────────────────────────────────────────
#  STYLE SPÉCIFIQUE COMPARATEUR
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── METRIC CARDS ── */
    .metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
    .metric-card {
        flex: 1;
        background: rgba(0, 25, 50, 0.65);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid;
        text-align: center;
    }
    .card-added    { border-left-color: #00C853; }
    .card-removed  { border-left-color: #FF3D00; }
    .card-modified { border-left-color: #FFD600; }
    .card-identical{ border-left-color: #455A64; }
    .metric-number { font-size: 2.2rem; font-weight: 800; margin: 0; }
    .metric-label  { font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; }
    .color-added    { color: #00C853; }
    .color-removed  { color: #FF3D00; }
    .color-modified { color: #FFD600; }
    .color-identical{ color: #546E7A; }

    /* ── FILE UPLOADER — override global pour lisibilité ── */
    [data-testid="stFileUploader"] {
        background: rgba(0, 212, 255, 0.06) !important;
        border: 2px dashed rgba(0, 212, 255, 0.4) !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stFileDropzoneInstructions"],
    [data-testid="stFileDropzoneInstructions"] span,
    [data-testid="stFileDropzoneInstructions"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: rgba(255, 255, 255, 0.75) !important;
    }
    /* Bouton Browse — visible sur fond sombre */
    [data-testid="stFileUploader"] button,
    [data-testid="stBaseButton-secondary"] {
        background: rgba(0, 212, 255, 0.15) !important;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
        color: #00D4FF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background: rgba(0, 212, 255, 0.25) !important;
    }

    /* ── SELECTBOX ── */
    [data-testid="stSelectbox"] > div > div {
        background: rgba(0, 25, 50, 0.7) !important;
        border: 1px solid rgba(0, 212, 255, 0.35) !important;
        color: white !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTES — chemins vanilla embarqués
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
VANILLA_PATHS = {
    "Chernarus": BASE_DIR / "data" / "vanilla" / "chernarus" / "types.xml",
    "Livonia":   BASE_DIR / "data" / "vanilla" / "livonia"   / "types.xml",
    "Sakhal":    BASE_DIR / "data" / "vanilla" / "sakhal"    / "types.xml",
}

# ─────────────────────────────────────────────
#  PARSING
# ─────────────────────────────────────────────
SIMPLE_FIELDS = ["nominal", "lifetime", "restock", "min",
                 "quantmin", "quantmax", "cost"]
FLAG_FIELDS   = ["count_in_cargo", "count_in_hoarder", "count_in_map",
                 "count_in_player", "crafted", "deloot"]

def parse_types_xml(content: bytes) -> dict:
    """
    Parse un types.xml → dict { classname: {champs} }
    Gère : champs simples, flags, category, usage (liste), value (liste)
    """
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        st.error(f"❌ Erreur XML : {e}")
        return {}

    items = {}
    for type_elem in root.findall("type"):
        name = type_elem.get("name", "").strip()
        if not name:
            continue

        data = {}

        # Champs simples
        for field in SIMPLE_FIELDS:
            elem = type_elem.find(field)
            data[field] = int(elem.text) if elem is not None and elem.text else 0

        # Flags (attributs d'une balise unique)
        flags_elem = type_elem.find("flags")
        if flags_elem is not None:
            for flag in FLAG_FIELDS:
                data[f"flag_{flag}"] = flags_elem.get(flag, "0")
        else:
            for flag in FLAG_FIELDS:
                data[f"flag_{flag}"] = "0"

        # Category (unique)
        cat = type_elem.find("category")
        data["category"] = cat.get("name", "") if cat is not None else ""

        # Usage (multiple) → liste triée pour comparaison stable
        data["usage"] = sorted([u.get("name", "") for u in type_elem.findall("usage")])

        # Value/tier (multiple) → liste triée
        data["value"] = sorted([v.get("name", "") for v in type_elem.findall("value")])

        items[name] = data

    return items


# ─────────────────────────────────────────────
#  COMPARAISON
# ─────────────────────────────────────────────
def compare_items(vanilla: dict, custom: dict) -> dict:
    """
    Retourne 4 listes :
    - added    : dans custom, absent du vanilla
    - removed  : dans vanilla, absent du custom
    - modified : présent des 2 côtés, au moins un champ différent
    - identical: présent des 2 côtés, aucune différence
    """
    all_keys = set(vanilla) | set(custom)
    result = {"added": [], "removed": [], "modified": [], "identical": []}

    for key in sorted(all_keys):
        in_vanilla = key in vanilla
        in_custom  = key in custom

        if in_custom and not in_vanilla:
            result["added"].append({"classname": key, **custom[key]})
        elif in_vanilla and not in_custom:
            result["removed"].append({"classname": key, **vanilla[key]})
        else:
            v, c = vanilla[key], custom[key]
            diffs = {}
            for field in SIMPLE_FIELDS + [f"flag_{f}" for f in FLAG_FIELDS] + ["category", "usage", "value"]:
                if v.get(field) != c.get(field):
                    diffs[field] = {"vanilla": v.get(field), "custom": c.get(field)}
            if diffs:
                result["modified"].append({
                    "classname": key,
                    "diffs": diffs,
                    "vanilla": v,
                    "custom": c,
                })
            else:
                result["identical"].append(key)

    return result


# ─────────────────────────────────────────────
#  EXPORT EXCEL
# ─────────────────────────────────────────────
def build_excel(result: dict, map_name: str) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Onglet Ajoutés
        if result["added"]:
            df = pd.DataFrame(result["added"])
            df["usage"] = df["usage"].apply(lambda x: ", ".join(x))
            df["value"] = df["value"].apply(lambda x: ", ".join(x))
            df.to_excel(writer, sheet_name="✅ Ajoutés", index=False)

        # Onglet Supprimés
        if result["removed"]:
            df = pd.DataFrame(result["removed"])
            df["usage"] = df["usage"].apply(lambda x: ", ".join(x))
            df["value"] = df["value"].apply(lambda x: ", ".join(x))
            df.to_excel(writer, sheet_name="❌ Supprimés", index=False)

        # Onglet Modifiés — vue lisible
        if result["modified"]:
            rows = []
            for item in result["modified"]:
                for field, vals in item["diffs"].items():
                    rows.append({
                        "classname": item["classname"],
                        "champ": field,
                        "valeur_vanilla": str(vals["vanilla"]),
                        "valeur_custom": str(vals["custom"]),
                    })
            pd.DataFrame(rows).to_excel(writer, sheet_name="⚠️ Modifiés", index=False)

        # Onglet résumé
        summary = pd.DataFrame([{
            "map": map_name,
            "ajoutés": len(result["added"]),
            "supprimés": len(result["removed"]),
            "modifiés": len(result["modified"]),
            "identiques": len(result["identical"]),
            "total_custom": len(result["added"]) + len(result["modified"]) + len(result["identical"]),
        }])
        summary.to_excel(writer, sheet_name="📊 Résumé", index=False)

    return output.getvalue()


st.divider()

# ─────────────────────────────────────────────
#  SÉLECTION MAP + UPLOAD
# ─────────────────────────────────────────────
col_map, col_upload = st.columns([1, 2])

with col_map:
    st.markdown("**🗺️ Sélectionne ta map**")
    map_name = st.selectbox(
        "Map",
        options=list(VANILLA_PATHS.keys()),
        label_visibility="collapsed"
    )

    vanilla_path = VANILLA_PATHS[map_name]
    if vanilla_path.exists():
        st.success(f"✅ Vanilla {map_name} chargé ({vanilla_path.stat().st_size // 1024} Ko)")
    else:
        st.error(f"❌ Fichier vanilla introuvable : `{vanilla_path}`")
        st.stop()

with col_upload:
    st.markdown("**📂 Upload ton types.xml custom**")
    uploaded = st.file_uploader(
        "types.xml",
        type=["xml"],
        label_visibility="collapsed",
        help="Upload uniquement ton fichier types.xml modifié"
    )

# ─────────────────────────────────────────────
#  TRAITEMENT
# ─────────────────────────────────────────────
if not uploaded:
    st.info("⬆️ Upload ton fichier types.xml custom pour lancer la comparaison.")
    st.stop()

# Parsing
with st.spinner("Analyse en cours..."):
    vanilla_data = parse_types_xml(vanilla_path.read_bytes())
    custom_data  = parse_types_xml(uploaded.read())

if not vanilla_data or not custom_data:
    st.stop()

result = compare_items(vanilla_data, custom_data)

# ─────────────────────────────────────────────
#  MÉTRIQUES RÉSUMÉ
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card card-added">
        <p class="metric-number color-added">{len(result['added'])}</p>
        <p class="metric-label">Ajoutés</p>
    </div>
    <div class="metric-card card-removed">
        <p class="metric-number color-removed">{len(result['removed'])}</p>
        <p class="metric-label">Supprimés</p>
    </div>
    <div class="metric-card card-modified">
        <p class="metric-number color-modified">{len(result['modified'])}</p>
        <p class="metric-label">Modifiés</p>
    </div>
    <div class="metric-card card-identical">
        <p class="metric-number color-identical">{len(result['identical'])}</p>
        <p class="metric-label">Identiques</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Export Excel
excel_bytes = build_excel(result, map_name)
st.download_button(
    label="📥 Exporter le rapport Excel",
    data=excel_bytes,
    file_name=f"codex_diff_{map_name.lower()}_{uploaded.name}".replace(".xml", ".xlsx"),
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.divider()

# ─────────────────────────────────────────────
#  ONGLETS RÉSULTATS
# ─────────────────────────────────────────────
tab_modified, tab_added, tab_removed = st.tabs([
    f"⚠️ Modifiés ({len(result['modified'])})",
    f"🟢 Ajoutés ({len(result['added'])})",
    f"🔴 Supprimés ({len(result['removed'])})",
])

# ── MODIFIÉS ──────────────────────────────────
with tab_modified:
    if not result["modified"]:
        st.success("Aucune modification détectée.")
    else:
        # Filtre recherche
        search = st.text_input("🔎 Rechercher un item", placeholder="ex: AK101, Pistol...", key="search_mod")
        items_mod = result["modified"]
        if search:
            items_mod = [i for i in items_mod if search.lower() in i["classname"].lower()]

        st.caption(f"{len(items_mod)} item(s) affiché(s)")

        for item in items_mod:
            with st.expander(f"**{item['classname']}** — {len(item['diffs'])} champ(s) modifié(s)"):
                rows = []
                for field, vals in item["diffs"].items():
                    v_val = ", ".join(vals["vanilla"]) if isinstance(vals["vanilla"], list) else str(vals["vanilla"])
                    c_val = ", ".join(vals["custom"])  if isinstance(vals["custom"],  list) else str(vals["custom"])
                    rows.append({"Champ": field, "Vanilla": v_val, "Custom ✏️": c_val})

                df = pd.DataFrame(rows)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Champ":     st.column_config.TextColumn(width="medium"),
                        "Vanilla":   st.column_config.TextColumn(width="medium"),
                        "Custom ✏️": st.column_config.TextColumn(width="medium"),
                    }
                )

# ── AJOUTÉS ───────────────────────────────────
with tab_added:
    if not result["added"]:
        st.info("Aucun item ajouté par rapport au vanilla.")
    else:
        search_add = st.text_input("🔎 Rechercher", placeholder="ex: M4A1...", key="search_add")
        items_add = result["added"]
        if search_add:
            items_add = [i for i in items_add if search_add.lower() in i["classname"].lower()]

        df = pd.DataFrame(items_add)
        df["usage"] = df["usage"].apply(lambda x: ", ".join(x))
        df["value"] = df["value"].apply(lambda x: ", ".join(x))
        st.caption(f"{len(items_add)} item(s) affiché(s)")
        st.dataframe(df, use_container_width=True, hide_index=True)

# ── SUPPRIMÉS ─────────────────────────────────
with tab_removed:
    if not result["removed"]:
        st.info("Aucun item vanilla supprimé.")
    else:
        search_rem = st.text_input("🔎 Rechercher", placeholder="ex: AK74...", key="search_rem")
        items_rem = result["removed"]
        if search_rem:
            items_rem = [i for i in items_rem if search_rem.lower() in i["classname"].lower()]

        df = pd.DataFrame(items_rem)
        df["usage"] = df["usage"].apply(lambda x: ", ".join(x))
        df["value"] = df["value"].apply(lambda x: ", ".join(x))
        st.caption(f"{len(items_rem)} item(s) affiché(s)")
        st.dataframe(df, use_container_width=True, hide_index=True)
