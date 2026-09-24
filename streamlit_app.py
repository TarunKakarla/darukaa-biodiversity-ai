import json
import uuid
from typing import Any, Dict, Optional

import streamlit as st
from dotenv import load_dotenv

from app.models import EnvironmentalMetrics
from app.pipeline import process
from app.memory.session import get_session_summary, reset_session

# =========================================================
# Environment & Page Configuration
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="Darukaa.Earth — AI Biodiversity Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# Premium Custom Styling
# =========================================================

st.markdown(
    """
    <style>
    /* Metric & Nexus Pills */
    .nexus-badge {
        display: inline-block;
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        color: #ecfdf5;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid #10b981;
    }
    .risk-critical {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #f87171;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .risk-high {
        background-color: #ffedd5;
        color: #9a3412;
        border: 1px solid #fb923c;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .risk-moderate {
        background-color: #fef9c3;
        color: #854d0e;
        border: 1px solid #facc15;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .causal-step {
        display: inline-block;
        background: #f1f5f9;
        color: #0f172a;
        padding: 6px 12px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 3px;
    }
    .causal-arrow {
        color: #10b981;
        font-weight: 800;
        margin: 0 4px;
    }
    .card-container {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        background-color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .source-box {
        background-color: #f8fafc;
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Session State Initialization
# =========================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Environmental Metrics default states
default_params = {
    "soil_ph": 7.0,
    "soil_organic_carbon": 0.3,
    "soil_moisture": "low",
    "bulk_density": 1.45,
    "land_use_type": "monoculture",
    "crop": "monoculture wheat",
    "canopy_cover": 5.0,
    "species_richness": 6.0,
    "habitat_diversity": 0.2,
    "pollinator_density": "depleted",
    "temperature": 26.0,
    "rainfall": "low",
    "region": "semi-arid",
    "pollution": "low agrochemical",
    "deforestation": "none",
    "latitude": 31.5,
    "longitude": 74.3,
    "ecoregion": "Semi-Arid Steppe / Indo-Gangetic Dryland",
}

for k, v in default_params.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_new_conversation():
    """
    Clears conversation memory and regenerates session state.
    """
    reset_session(st.session_state.session_id)
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()


def load_preset(preset_name: str):
    """
    Loads specific ecosystem presets including the hackathon example.
    """
    if preset_name == "hackathon_example":
        st.session_state.soil_ph = 7.2
        st.session_state.soil_organic_carbon = 0.3
        st.session_state.soil_moisture = "low"
        st.session_state.land_use_type = "monoculture"
        st.session_state.crop = "monoculture wheat"
        st.session_state.rainfall = "low"
        st.session_state.region = "semi-arid"
        st.session_state.species_richness = 5.0
        st.session_state.habitat_diversity = 0.15
        st.session_state.temperature = 28.0
        st.session_state.ecoregion = "Semi-Arid Dryland (FAO Agroecology Case)"
        st.success("Loaded: Hackathon Example (SOC 0.3%, low rainfall, monoculture wheat, semi-arid)!")

    elif preset_name == "degraded_acidic":
        st.session_state.soil_ph = 5.1
        st.session_state.soil_organic_carbon = 0.45
        st.session_state.soil_moisture = "medium"
        st.session_state.land_use_type = "intensive cropland"
        st.session_state.crop = "corn monoculture"
        st.session_state.rainfall = "medium"
        st.session_state.region = "temperate"
        st.session_state.pollution = "high pesticide runoff"
        st.session_state.species_richness = 3.0
        st.session_state.habitat_diversity = 0.1
        st.session_state.ecoregion = "Temperate Intensive Cropland"
        st.success("Loaded: Degraded Acidic Agroecosystem!")

    elif preset_name == "mediterranean_dryland":
        st.session_state.soil_ph = 7.8
        st.session_state.soil_organic_carbon = 0.55
        st.session_state.soil_moisture = "scarce"
        st.session_state.land_use_type = "cereal-olive mosaic"
        st.session_state.crop = "barley"
        st.session_state.rainfall = "low"
        st.session_state.region = "mediterranean"
        st.session_state.temperature = 31.0
        st.session_state.species_richness = 8.0
        st.session_state.habitat_diversity = 0.3
        st.session_state.ecoregion = "Mediterranean Arid Basin"
        st.success("Loaded: Mediterranean Dryland!")

    st.rerun()


def build_metrics_from_state() -> EnvironmentalMetrics:
    """
    Constructs the EnvironmentalMetrics model from the sidebar/session parameters.
    """
    return EnvironmentalMetrics(
        soil_ph=st.session_state.soil_ph,
        soil_organic_carbon=st.session_state.soil_organic_carbon,
        soil_moisture=st.session_state.soil_moisture or None,
        bulk_density=st.session_state.bulk_density or None,
        land_use_type=st.session_state.land_use_type or None,
        crop=st.session_state.crop or None,
        canopy_cover=st.session_state.canopy_cover or None,
        species_richness=st.session_state.species_richness,
        habitat_diversity=st.session_state.habitat_diversity,
        pollinator_density=st.session_state.pollinator_density or None,
        temperature=st.session_state.temperature,
        rainfall=st.session_state.rainfall or None,
        region=st.session_state.region or None,
        pollution=st.session_state.pollution or None,
        deforestation=st.session_state.deforestation or None,
        latitude=st.session_state.latitude,
        longitude=st.session_state.longitude,
        ecoregion=st.session_state.ecoregion or None,
    )


# =========================================================
# Sidebar Controls & Context
# =========================================================

with st.sidebar:
    st.markdown("### 🌿 Ecosystem Control Panel")
    st.caption("AI-Powered Biodiversity & Environmental Intelligence")

    # -----------------------------------------------------
    # Memory Inspector Section (Explicit User Request)
    # -----------------------------------------------------
    st.divider()
    st.markdown("#### 🧠 Session Memory")

    session_summary = get_session_summary(st.session_state.session_id)
    turns_count = session_summary.get("total_turns", 0)

    col_mem1, col_mem2 = st.columns(2)
    with col_mem1:
        st.metric("Session Turns", turns_count)
    with col_mem2:
        st.metric("Status", "🟢 Active" if turns_count > 0 else "Ready")

    with st.expander("🔍 Inspect Remembered Context", expanded=False):
        st.caption(f"**Session ID:** `{st.session_state.session_id[:12]}...`")
        remembered_metrics = session_summary.get("environmental_state", {})
        if remembered_metrics:
            st.markdown("**Accumulated Variables:**")
            for k, v in list(remembered_metrics.items())[:8]:
                st.write(f"- `{k}`: {v}")
        else:
            st.write("No prior dialogue turns recorded yet.")

        prior_recs = session_summary.get("prior_recommendations", [])
        if prior_recs:
            st.markdown("**Remembered Practices:**")
            for pr in prior_recs[:3]:
                st.write(f"- {pr}")

    if st.button("🔄 Reset Session Memory", use_container_width=True):
        start_new_conversation()

    # -----------------------------------------------------
    # Structured Input Presets (Core Requirement 5)
    # -----------------------------------------------------
    st.divider()
    st.markdown("#### 📥 Structured Presets & JSON")

    preset_choice = st.selectbox(
        "Load Environmental Preset:",
        [
            "Select a preset...",
            "Hackathon Example (SOC 0.3%, Low Rain, Semi-Arid)",
            "Degraded Acidic Cropland (pH 5.1, Pesticide Stress)",
            "Mediterranean Dryland (Barley, Low Rain, Heat)",
        ],
        index=0,
    )

    if preset_choice.startswith("Hackathon Example"):
        if st.button("Apply Hackathon Preset", use_container_width=True):
            load_preset("hackathon_example")
    elif preset_choice.startswith("Degraded Acidic"):
        if st.button("Apply Degraded Acidic Preset", use_container_width=True):
            load_preset("degraded_acidic")
    elif preset_choice.startswith("Mediterranean"):
        if st.button("Apply Mediterranean Preset", use_container_width=True):
            load_preset("mediterranean_dryland")

    with st.expander("📋 Paste Custom JSON Input"):
        json_input = st.text_area(
            "Paste Environmental JSON:",
            value="",
            placeholder='{"soil_organic_carbon": 0.3, "rainfall": "low", "crop": "monoculture wheat", "region": "semi-arid"}',
            height=100
        )
        if st.button("Load JSON into Session", use_container_width=True):
            try:
                parsed = json.loads(json_input)
                for pk, pv in parsed.items():
                    if pk in st.session_state:
                        st.session_state[pk] = pv
                st.success("Loaded JSON parameters!")
                st.rerun()
            except Exception as e:
                st.error(f"Invalid JSON: {e}")

    # -----------------------------------------------------
    # Environmental Variable Parameters
    # -----------------------------------------------------
    st.divider()
    st.markdown("#### 🌍 Environmental Parameters")

    # 1. Soil Health
    with st.expander("🌱 1. Soil Health Metrics", expanded=True):
        st.number_input("Soil Organic Carbon (%)", min_value=0.0, max_value=15.0, step=0.1, key="soil_organic_carbon")
        st.number_input("Soil pH", min_value=0.0, max_value=14.0, step=0.1, key="soil_ph")
        st.selectbox("Soil Moisture", ["low", "moderate", "high", "waterlogged", "unknown"], index=0, key="soil_moisture")
        st.number_input("Bulk Density (g/cm³)", min_value=0.5, max_value=2.2, step=0.05, key="bulk_density")

    # 2. Land Use & Crop
    with st.expander("🌾 2. Land Use & Agriculture", expanded=True):
        st.text_input("Land Use Type", key="land_use_type")
        st.text_input("Current Crop", key="crop")
        st.number_input("Canopy Cover (%)", min_value=0.0, max_value=100.0, step=1.0, key="canopy_cover")

    # 3. Biodiversity Indicators
    with st.expander("🦋 3. Biodiversity Indicators", expanded=False):
        st.number_input("Species Richness Index", min_value=0.0, max_value=200.0, step=1.0, key="species_richness")
        st.number_input("Habitat Heterogeneity (0-1)", min_value=0.0, max_value=1.0, step=0.05, key="habitat_diversity")
        st.selectbox("Pollinator Status", ["depleted", "low", "moderate", "abundant"], index=0, key="pollinator_density")

    # 4. Climate & Hydrology
    with st.expander("🌦️ 4. Climate & Hydrology", expanded=False):
        st.selectbox("Rainfall Regime", ["low", "medium", "high", "variable"], index=0, key="rainfall")
        st.number_input("Mean Temperature (°C)", min_value=-20.0, max_value=55.0, step=0.5, key="temperature")
        st.text_input("Climate Region / Aridity", key="region")

    # 5. Human Pressures & Spatial Context (Bonus Feature)
    with st.expander("📍 5. Spatial & Human Stressors", expanded=False):
        st.text_input("Pollution / Chemical Load", key="pollution")
        st.text_input("Deforestation / Canopy Loss", key="deforestation")
        st.markdown("**Spatial Context (Bonus):**")
        st.text_input("Ecoregion / Biome", key="ecoregion")
        c_lat, c_lon = st.columns(2)
        with c_lat:
            st.number_input("Latitude", step=0.1, key="latitude")
        with c_lon:
            st.number_input("Longitude", step=0.1, key="longitude")

        if st.session_state.latitude is not None and st.session_state.longitude is not None:
            import pandas as pd
            try:
                map_df = pd.DataFrame([{"lat": float(st.session_state.latitude), "lon": float(st.session_state.longitude)}])
                st.map(map_df, zoom=3)
            except Exception:
                pass

    # -----------------------------------------------------
    # AI Engine Configuration
    # -----------------------------------------------------
    st.divider()
    with st.expander("⚙️ AI Engine & API Configuration"):
        has_groq_secret = False
        try:
            if hasattr(st, "secrets") and ("GROQ_API_KEY" in st.secrets or "OPENAI_API_KEY" in st.secrets):
                has_groq_secret = True
        except Exception:
            pass

        if has_groq_secret:
            st.success("🟢 Cloud API Connected (via Streamlit Secrets)")

        engine_mode = st.selectbox(
            "Reasoning Engine:",
            [
                "Cloud Secrets / Autonomous Scientific Engine (Recommended)",
                "Custom LLM API (Groq / OpenAI / OpenRouter / LM Studio)"
            ],
            index=0
        )
        custom_api_key = ""
        custom_base_url = ""
        custom_model = ""

        if "Custom" in engine_mode:
            custom_api_key = st.text_input("API Key (e.g. Groq gsk_... or OpenAI):", type="password")
            custom_base_url = st.text_input("Base URL:", placeholder="https://api.groq.com/openai/v1")
            custom_model = st.text_input("Model:", placeholder="llama-3.3-70b-versatile")


# =========================================================
# Main UI Display Functions
# =========================================================

def render_evidence_cards(evidence_list):
    """
    Renders verifiable evidence items with source titles, URLs, and pages.
    """
    if not evidence_list:
        return

    for item in evidence_list:
        if not isinstance(item, dict):
            continue
        title = item.get("source_title", "Authoritative Environmental Report")
        page = item.get("page_number")
        excerpt = item.get("supporting_excerpt_or_summary") or item.get("excerpt", "")
        url = item.get("source_url") or item.get("url")

        st.markdown(
            f"""
            <div class="source-box">
                <b>📖 {title}</b> {f'(Page {page})' if page else ''}<br>
                <i>"{excerpt}"</i><br>
                {f'<a href="{url}" target="_blank">🔗 View Official Document</a>' if url else ''}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_response(result: Dict[str, Any]):
    """
    Displays structured, evidence-grounded response compliant with hackathon evaluation.
    """
    if not isinstance(result, dict):
        st.write(result)
        return

    resp_type = result.get("type")

    # -----------------------------------------------------
    # Clarification Response
    # -----------------------------------------------------
    if resp_type == "clarification":
        st.warning("⚠️ Environmental Information Incomplete")
        st.markdown(f"### ❓ {result.get('question', 'Additional information required.')}")
        st.markdown(
            """
            *As an AI Environmental Scientist, this system avoids generic guesswork. "
            "Accurate ecological recommendations require at least 3 coupled environmental variables.*
            """
        )
        missing = result.get("missing_metrics", [])
        if missing:
            st.markdown("**Parameters needed for multi-metric reasoning:**")
            for m in missing:
                st.markdown(f"- **{m.replace('_', ' ').capitalize()}**")

        st.info("💡 You can provide these parameters directly in your next chat message or adjust them in the sidebar!")
        if st.button("🌱 Autofill with Hackathon Baseline Parameters (SOC 0.3%, Low Rain, Monoculture Wheat)", key=f"autofill_{result.get('session_id', 'clar')}"):
            load_preset("hackathon_example")
        return

    # -----------------------------------------------------
    # Recommendations Response
    # -----------------------------------------------------
    if resp_type == "recommendations":

        # 1. Multi-Metric Nexus Header
        nexus = result.get("multi_metric_nexus")
        if nexus and isinstance(nexus, dict):
            coupled = nexus.get("coupled_variables", [])
            risk = nexus.get("compound_risk", "Moderate")

            risk_class = "risk-critical" if "Critical" in risk else ("risk-high" if "High" in risk else "risk-moderate")

            st.markdown("#### 🔗 Multi-Metric Ecological Nexus")
            st.markdown(
                f"""
                <div style="margin-bottom: 12px;">
                    <span class="{risk_class}">Compound Risk: {risk}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if coupled:
                pills_html = " ".join([f'<span class="nexus-badge">{var}</span>' for var in coupled])
                st.markdown(f"<div>{pills_html}</div>", unsafe_allow_html=True)

            pathway = nexus.get("ecological_pathway")
            if pathway:
                st.caption(f"**Degradation Loop:** {pathway}")

        # 2. Executive Scientific Assessment
        summary = result.get("summary")
        if summary:
            st.markdown("### 🌿 Scientific Assessment")
            st.markdown(f">{summary}")

        # 3. Actionable Recommendations
        recommendations = result.get("recommendations", [])
        if recommendations:
            st.markdown("### 💡 Evidence-Backed Recommendations")

            for i, rec in enumerate(recommendations, start=1):
                if not isinstance(rec, dict):
                    continue

                what_to_do = rec.get("what_to_do", f"Recommendation {i}")
                why_it_works = rec.get("why_it_works", "")
                causal_chain = rec.get("causal_chain", [])
                impacted = rec.get("impacted_metrics", [])
                time_horizon = rec.get("time_horizon", "medium")
                confidence = rec.get("confidence", "high")
                measurable = rec.get("measurable_impact", "")
                trade_offs = rec.get("trade_offs_or_prerequisites", "")
                evidence = rec.get("evidence", [])

                with st.container():
                    st.markdown(f"#### {i}. {what_to_do}")

                    # Metadata Badges
                    col_b1, col_b2, col_b3 = st.columns([1, 1, 2])
                    with col_b1:
                        st.markdown(f"⏱️ **Horizon:** `{str(time_horizon).capitalize()}`")
                    with col_b2:
                        st.markdown(f"🎯 **Confidence:** `{str(confidence).capitalize()}`")
                    with col_b3:
                        if impacted:
                            st.markdown(f"📊 **Metrics:** `{', '.join(impacted[:3])}`")

                    # Why it works
                    if why_it_works:
                        st.markdown(f"**Ecological Mechanism:** {why_it_works}")

                    # Causal Chain Visualization
                    if causal_chain:
                        chain_html = '<div style="margin: 8px 0;">'
                        for idx, step in enumerate(causal_chain):
                            chain_html += f'<span class="causal-step">{step}</span>'
                            if idx < len(causal_chain) - 1:
                                chain_html += '<span class="causal-arrow">→</span>'
                        chain_html += '</div>'
                        st.markdown(chain_html, unsafe_allow_html=True)

                    # Measurable Impact
                    if measurable:
                        st.markdown(f"📈 **Measurable Impact:** `{measurable}`")

                    # Trade-offs / Prerequisites
                    if trade_offs:
                        st.caption(f"⚖️ **Prerequisites / Trade-offs:** {trade_offs}")

                    # Evidence
                    if evidence:
                        with st.expander("📚 Supporting Scientific Evidence & Citations"):
                            render_evidence_cards(evidence)

                    st.divider()

        # 4. Retrieved Scientific Literature Drawer
        sources = result.get("retrieved_sources", [])
        if sources:
            with st.expander("🔎 View Retrieved RAG Sources (ChromaDB + Knowledge Base)", expanded=False):
                for s_idx, s in enumerate(sources[:6], start=1):
                    s_title = s.get("source_title", f"Scientific Source {s_idx}")
                    s_url = s.get("source_url", "")
                    s_page = s.get("page_number")
                    s_excerpt = s.get("supporting_excerpt_or_summary", "")

                    st.markdown(f"**{s_idx}. {s_title}** {f'(Page {s_page})' if s_page else ''}")
                    if s_excerpt:
                        st.caption(f'"{s_excerpt[:240]}..."')
                    if s_url:
                        st.markdown(f"[🔗 Open Official Source]({s_url})")
                    st.write("")

        # 5. Download Assessment Button
        res_json = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download Scientific Report (JSON)",
            data=res_json,
            file_name=f"darukaa_biodiversity_report_{st.session_state.session_id[:8]}.json",
            mime="application/json"
        )
        return

    st.json(result)


# =========================================================
# Main Page Header & Quick-Start Chips
# =========================================================

st.title("🌱 Darukaa.Earth — AI Biodiversity Intelligence")
st.markdown(
    """
    **Autonomous Environmental Science System** combining multi-variable ecological reasoning,
    causal graph modeling, hybrid RAG literature retrieval (FAO, IPCC, CBD, IPBES),
    and multi-turn conversational memory.
    """
)

# Quick scenario chips
col_chip1, col_chip2, col_chip3 = st.columns(3)
with col_chip1:
    if st.button("🌱 Hackathon Case (SOC 0.3%, Semi-Arid)", use_container_width=True):
        st.session_state.preset_query = "Suggest agroforestry and intercropping recommendations for low SOC semi-arid wheat monoculture."
with col_chip2:
    if st.button("🌳 Agroforestry & Pollinators Query", use_container_width=True):
        st.session_state.preset_query = "How can agroforestry help restore pollinator diversity and water holding capacity?"
with col_chip3:
    if st.button("❓ Test Incomplete Input Clarification", use_container_width=True):
        st.session_state.preset_query = "Biodiversity is declining on my land. What can I do?"

# =========================================================
# Chat History
# =========================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            render_response(msg["content"])

# =========================================================
# Chat Input & Pipeline Execution
# =========================================================

# Check if a preset query button was clicked
preset_text = st.session_state.pop("preset_query", None)
user_query = st.chat_input("Ask a biodiversity, soil health, or agroecological question...") or preset_text

if user_query:
    # 1. Build current environmental metrics from sidebar/state
    metrics = build_metrics_from_state()

    # 2. Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append({"role": "user", "content": user_query})

    # 3. Process via pipeline
    with st.chat_message("assistant"):
        with st.spinner("🔬 AI Environmental Scientist is analyzing ecological nexus & retrieving evidence..."):
            try:
                # Resolve custom API keys if provided
                opt_key = custom_api_key if "Custom" in engine_mode and custom_api_key else None
                opt_base = custom_base_url if "Custom" in engine_mode and custom_base_url else None
                opt_model = custom_model if "Custom" in engine_mode and custom_model else None

                response = process(
                    session_id=st.session_state.session_id,
                    metrics=metrics,
                    message=user_query,
                    api_key=opt_key,
                    base_url=opt_base,
                    model_name=opt_model,
                )

                render_response(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error("Failed to complete environmental reasoning.")
                st.exception(e)