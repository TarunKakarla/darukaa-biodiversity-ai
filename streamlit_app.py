import uuid

import streamlit as st
from dotenv import load_dotenv

from app.models import EnvironmentalMetrics
from app.pipeline import process


# =========================================================
# Environment
# =========================================================

load_dotenv()


# =========================================================
# Streamlit Configuration
# =========================================================

st.set_page_config(
    page_title="Darukaa Earth AI Environmental Scientist",
    page_icon="🌱",
    layout="wide",
)


# =========================================================
# Session State
# =========================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# Helper: Create Environmental Metrics
# =========================================================

def create_metrics(
    soil_ph,
    soil_organic_carbon,
    soil_moisture,
    land_use_type,
    crop,
    species_richness,
    habitat_diversity,
    temperature,
    rainfall,
    pollution,
    deforestation,
    region,
):
    return EnvironmentalMetrics(
        soil_ph=soil_ph,
        soil_organic_carbon=soil_organic_carbon,
        soil_moisture=soil_moisture or None,
        land_use_type=land_use_type or None,
        crop=crop or None,
        species_richness=species_richness,
        habitat_diversity=habitat_diversity,
        temperature=temperature,
        rainfall=rainfall or None,
        pollution=pollution or None,
        deforestation=deforestation or None,
        region=region or None,
    )


# =========================================================
# Helper: Display Evidence
# =========================================================

def display_evidence(evidence):
    if not evidence:
        return

    for i, item in enumerate(evidence, start=1):

        if not isinstance(item, dict):
            st.write(item)
            continue

        title = (
            item.get("source_title")
            or item.get("title")
            or f"Evidence {i}"
        )

        page = item.get("page_number")

        excerpt = (
            item.get("supporting_excerpt_or_summary")
            or item.get("excerpt")
            or item.get("summary")
        )

        url = (
            item.get("source_url")
            or item.get("url")
        )

        with st.expander(f"Evidence {i}: {title}"):

            if page is not None:
                st.write(f"**Page:** {page}")

            if excerpt:
                st.write(f"**Evidence:** {excerpt}")

            if url:
                st.markdown(f"[Open source]({url})")


# =========================================================
# Helper: Display Retrieved Sources
# =========================================================

def display_sources(sources):
    if not sources:
        return

    st.subheader("📚 Retrieved Scientific Sources")

    for i, source in enumerate(sources, start=1):

        if not isinstance(source, dict):
            st.write(source)
            continue

        title = (
            source.get("source_title")
            or source.get("title")
            or f"Source {i}"
        )

        page = source.get("page_number")

        excerpt = (
            source.get("supporting_excerpt_or_summary")
            or source.get("excerpt")
            or source.get("summary")
        )

        url = (
            source.get("source_url")
            or source.get("url")
        )

        with st.expander(f"{i}. {title}"):

            if page is not None:
                st.write(f"**Page:** {page}")

            if excerpt:
                st.write(f"**Evidence:** {excerpt}")

            if url:
                st.markdown(f"[Open source]({url})")


# =========================================================
# Helper: Display Complete Pipeline Result
# =========================================================

def display_result(result):

    if not isinstance(result, dict):
        st.write(result)
        return

    response_type = result.get("type")

    # -----------------------------------------------------
    # Clarification
    # -----------------------------------------------------

    if response_type == "clarification":

        st.info("Additional environmental information is required.")

        question = result.get("question")

        if question:
            st.markdown(f"### ❓ {question}")

        missing_metrics = result.get(
            "missing_metrics",
            [],
        )

        if missing_metrics:

            st.write("**Missing metrics:**")

            for metric in missing_metrics:
                st.write(f"- {metric}")

        return

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    if response_type == "recommendations":

        summary = result.get("summary")

        if summary:
            st.subheader("🌿 Scientific Assessment")
            st.write(summary)

        recommendations = result.get(
            "recommendations",
            [],
        )

        if recommendations:

            st.subheader("💡 Recommendations")

            for i, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                if not isinstance(recommendation, dict):
                    st.write(recommendation)
                    continue

                what_to_do = recommendation.get(
                    "what_to_do",
                    f"Recommendation {i}",
                )

                st.markdown(
                    f"### {i}. {what_to_do}"
                )

                why_it_works = recommendation.get(
                    "why_it_works"
                )

                if why_it_works:
                    st.markdown(
                        f"**Why it works:** {why_it_works}"
                    )

                # -----------------------------------------
                # Recommendation metadata
                # -----------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    time_horizon = recommendation.get(
                        "time_horizon"
                    )

                    if time_horizon:
                        st.metric(
                            "Time Horizon",
                            str(time_horizon).capitalize(),
                        )

                with col2:
                    confidence = recommendation.get(
                        "confidence"
                    )

                    if confidence:
                        st.metric(
                            "Confidence",
                            str(confidence).capitalize(),
                        )

                with col3:
                    impacted_metrics = recommendation.get(
                        "impacted_metrics",
                        [],
                    )

                    st.metric(
                        "Impacted Metrics",
                        len(impacted_metrics),
                    )

                # -----------------------------------------
                # Causal Chain
                # -----------------------------------------

                causal_chain = recommendation.get(
                    "causal_chain",
                    [],
                )

                if causal_chain:

                    st.markdown("**🔗 Causal Chain**")

                    st.write(
                        " → ".join(
                            str(step)
                            for step in causal_chain
                        )
                    )

                # -----------------------------------------
                # Impacted Metrics
                # -----------------------------------------

                if impacted_metrics:

                    st.markdown(
                        "**📊 Impacted Metrics**"
                    )

                    st.write(
                        ", ".join(
                            str(metric)
                            for metric in impacted_metrics
                        )
                    )

                # -----------------------------------------
                # Evidence
                # -----------------------------------------

                evidence = recommendation.get(
                    "evidence",
                    [],
                )

                if evidence:

                    st.markdown(
                        "**📖 Supporting Evidence**"
                    )

                    display_evidence(evidence)

                st.divider()

        # ---------------------------------------------
        # Sources
        # ---------------------------------------------

        display_sources(
            result.get(
                "retrieved_sources",
                [],
            )
        )

        return

    # -----------------------------------------------------
    # Unknown response
    # -----------------------------------------------------

    st.subheader("Response")
    st.json(result)


# =========================================================
# Header
# =========================================================

st.title(
    "🌱 Darukaa.Earth — Biodiversity Intelligence"
)

st.markdown(
    """
**AI-powered environmental intelligence** using
scientific evidence, RAG retrieval, causal reasoning,
and biodiversity-focused recommendations.
"""
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("🌍 Environmental Context")

    st.caption(
        "Provide environmental conditions that "
        "the reasoning pipeline can use."
    )

    st.divider()

    # -----------------------------------------------------
    # Soil
    # -----------------------------------------------------

    st.subheader("🌱 Soil")

    soil_ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1,
    )

    soil_organic_carbon = st.number_input(
        "Soil organic carbon (%)",
        min_value=0.0,
        value=0.3,
        step=0.1,
    )

    soil_moisture = st.text_input(
        "Soil moisture",
        value="unknown",
    )

    # -----------------------------------------------------
    # Land and Agriculture
    # -----------------------------------------------------

    st.subheader("🌾 Land & Agriculture")

    land_use_type = st.text_input(
        "Land use type",
        value="monoculture",
    )

    crop = st.text_input(
        "Crop",
        value="wheat",
    )

    species_richness = st.number_input(
        "Species richness",
        min_value=0.0,
        value=0.0,
        step=1.0,
    )

    habitat_diversity = st.number_input(
        "Habitat diversity",
        min_value=0.0,
        value=0.0,
        step=0.1,
    )

    # -----------------------------------------------------
    # Climate
    # -----------------------------------------------------

    st.subheader("🌦️ Climate")

    temperature = st.number_input(
        "Temperature (°C)",
        value=25.0,
        step=0.5,
    )

    rainfall = st.selectbox(
        "Rainfall",
        [
            "low",
            "medium",
            "high",
        ],
        index=1,
    )

    region = st.text_input(
        "Region",
        value="semi-arid",
    )

    # -----------------------------------------------------
    # Environmental Pressure
    # -----------------------------------------------------

    st.subheader("⚠️ Environmental Pressure")

    pollution = st.text_input(
        "Pollution",
        value="",
    )

    deforestation = st.text_input(
        "Deforestation",
        value="",
    )

    st.divider()

    # -----------------------------------------------------
    # Session Management
    # -----------------------------------------------------

    st.subheader("💬 Session")

    st.caption("Current Session ID")

    st.code(
        st.session_state.session_id,
        language="text",
    )

    if st.button(
        "🔄 Start New Session",
        use_container_width=True,
    ):

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.session_state.messages = []

        st.rerun()


# =========================================================
# Previous Messages
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        if message["role"] == "user":
            st.markdown(
                message["content"]
            )

        else:
            display_result(
                message["content"]
            )


# =========================================================
# Chat Input
# =========================================================

question = st.chat_input(
    "Ask a biodiversity or environmental question..."
)


# =========================================================
# Run Pipeline
# =========================================================

if question:

    # -----------------------------------------------------
    # Build EnvironmentalMetrics object
    # -----------------------------------------------------

    metrics = create_metrics(
        soil_ph=soil_ph,
        soil_organic_carbon=soil_organic_carbon,
        soil_moisture=soil_moisture,
        land_use_type=land_use_type,
        crop=crop,
        species_richness=species_richness,
        habitat_diversity=habitat_diversity,
        temperature=temperature,
        rainfall=rainfall,
        pollution=pollution,
        deforestation=deforestation,
        region=region,
    )

    # -----------------------------------------------------
    # Display User Message
    # -----------------------------------------------------

    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # -----------------------------------------------------
    # Run Existing RAG / Reasoning Pipeline
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Retrieving scientific evidence and generating recommendations..."
        ):

            try:

                result = process(
                    st.session_state.session_id,
                    metrics,
                    question,
                )

                display_result(result)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result,
                    }
                )

            except Exception as e:

                st.error(
                    "Failed to process the request."
                )

                st.exception(e)