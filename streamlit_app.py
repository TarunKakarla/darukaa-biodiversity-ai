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


def start_new_conversation():
    """
    Start a completely new conversation.
    """

    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []

    st.rerun()


# =========================================================
# Environmental Metrics
# =========================================================

def create_metrics():
    """
    Create the EnvironmentalMetrics object from
    the values currently selected in the sidebar.
    """

    return EnvironmentalMetrics(
        soil_ph=st.session_state.soil_ph,
        soil_organic_carbon=(
            st.session_state.soil_organic_carbon
        ),
        soil_moisture=(
            st.session_state.soil_moisture
            or None
        ),
        land_use_type=(
            st.session_state.land_use_type
            or None
        ),
        crop=(
            st.session_state.crop
            or None
        ),
        species_richness=(
            st.session_state.species_richness
        ),
        habitat_diversity=(
            st.session_state.habitat_diversity
        ),
        temperature=(
            st.session_state.temperature
        ),
        rainfall=(
            st.session_state.rainfall
            or None
        ),
        pollution=(
            st.session_state.pollution
            or None
        ),
        deforestation=(
            st.session_state.deforestation
            or None
        ),
        region=(
            st.session_state.region
            or None
        ),
    )


# =========================================================
# Evidence Display
# =========================================================

def display_evidence(evidence):
    """
    Display recommendation-level supporting evidence.
    """

    if not evidence:
        return

    for i, item in enumerate(
        evidence,
        start=1,
    ):

        if not isinstance(item, dict):
            st.write(item)
            continue

        title = (
            item.get("source_title")
            or item.get("title")
            or f"Evidence {i}"
        )

        page = item.get(
            "page_number"
        )

        excerpt = (
            item.get(
                "supporting_excerpt_or_summary"
            )
            or item.get("excerpt")
            or item.get("summary")
        )

        url = (
            item.get("source_url")
            or item.get("url")
        )

        with st.expander(
            f"📄 {title}"
        ):

            if page is not None:
                st.write(
                    f"**Page:** {page}"
                )

            if excerpt:
                st.write(
                    f"**Supporting evidence:** "
                    f"{excerpt}"
                )

            if url:
                st.markdown(
                    f"[🔗 Open source]({url})"
                )


# =========================================================
# Retrieved Sources Display
# =========================================================

def display_sources(
    sources,
    evidence_sources=None,
):
    """
    Display the scientific sources returned by the RAG
    pipeline.

    Page numbers are first taken directly from
    retrieved_sources.

    If a page number is missing there, the function checks
    recommendation-level evidence for the same source.
    """

    if not sources:
        return

    evidence_sources = evidence_sources or []


    # =====================================================
    # Build page-number lookup
    # =====================================================

    page_lookup = {}

    for evidence in evidence_sources:

        if not isinstance(
            evidence,
            dict,
        ):
            continue

        title = (
            evidence.get("source_title")
            or evidence.get("title")
        )

        url = (
            evidence.get("source_url")
            or evidence.get("url")
        )

        page = evidence.get(
            "page_number"
        )

        if page is None:
            continue

        if title:
            page_lookup[
                ("title", title.strip().lower())
            ] = page

        if url:
            page_lookup[
                ("url", url.strip())
            ] = page


    # =====================================================
    # Remove duplicate sources
    # =====================================================

    unique_sources = []
    seen = set()

    for source in sources:

        if not isinstance(
            source,
            dict,
        ):
            continue

        title = (
            source.get("source_title")
            or source.get("title")
            or ""
        )

        url = (
            source.get("source_url")
            or source.get("url")
            or ""
        )

        key = (
            title.strip().lower(),
            url.strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_sources.append(source)


    if not unique_sources:
        return


    # =====================================================
    # Display
    # =====================================================

    st.subheader(
        "📚 Scientific Sources"
    )

    for i, source in enumerate(
        unique_sources,
        start=1,
    ):

        title = (
            source.get("source_title")
            or source.get("title")
            or f"Source {i}"
        )

        url = (
            source.get("source_url")
            or source.get("url")
        )

        excerpt = (
            source.get(
                "supporting_excerpt_or_summary"
            )
            or source.get("excerpt")
            or source.get("summary")
        )


        # -------------------------------------------------
        # First use page number returned directly
        # by retrieved_sources.
        # -------------------------------------------------

        page = source.get(
            "page_number"
        )


        # -------------------------------------------------
        # If missing, search recommendation evidence.
        # -------------------------------------------------

        if page is None:

            if url:

                page = page_lookup.get(
                    (
                        "url",
                        url.strip(),
                    )
                )

            if page is None and title:

                page = page_lookup.get(
                    (
                        "title",
                        title.strip().lower(),
                    )
                )


        # -------------------------------------------------
        # Source card
        # -------------------------------------------------

        with st.expander(
            f"📄 {title}",
            expanded=True,
        ):

            if page is not None:

                st.markdown(
                    f"**Page:** {page}"
                )

            else:

                st.write(
                    "**Page:** Not provided by retrieved metadata"
                )

            if excerpt:

                st.markdown(
                    f"**Supporting evidence:** "
                    f"{excerpt}"
                )

            if url:

                st.markdown(
                    f"[🔗 Open report]({url})"
                )


# =========================================================
# Response Display
# =========================================================

def display_result(result):
    """
    Display the complete response returned by
    app.pipeline.process().
    """

    if not isinstance(
        result,
        dict,
    ):
        st.write(result)
        return


    response_type = result.get(
        "type"
    )


    # =====================================================
    # Clarification Response
    # =====================================================

    if response_type == "clarification":

        st.info(
            "Additional environmental information is required."
        )

        question = result.get(
            "question"
        )

        if question:

            st.markdown(
                f"### ❓ {question}"
            )

        missing_metrics = result.get(
            "missing_metrics",
            [],
        )

        if missing_metrics:

            st.write(
                "**Missing information:**"
            )

            for metric in missing_metrics:

                st.write(
                    f"- {metric}"
                )

        return


    # =====================================================
    # Recommendation Response
    # =====================================================

    if response_type == "recommendations":

        # -------------------------------------------------
        # Scientific Assessment
        # -------------------------------------------------

        summary = result.get(
            "summary"
        )

        if summary:

            st.subheader(
                "🌿 Scientific Assessment"
            )

            st.write(
                summary
            )


        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        recommendations = result.get(
            "recommendations",
            [],
        )


        # -------------------------------------------------
        # Collect recommendation evidence
        # for page-number recovery.
        # -------------------------------------------------

        evidence_sources = []


        for recommendation in recommendations:

            if not isinstance(
                recommendation,
                dict,
            ):
                continue

            evidence_sources.extend(
                recommendation.get(
                    "evidence",
                    [],
                )
            )


        if recommendations:

            st.subheader(
                "💡 Recommendations"
            )


            for i, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                if not isinstance(
                    recommendation,
                    dict,
                ):

                    st.write(
                        recommendation
                    )

                    continue


                # =========================================
                # What to do
                # =========================================

                what_to_do = recommendation.get(
                    "what_to_do",
                    f"Recommendation {i}",
                )

                st.markdown(
                    f"### {i}. {what_to_do}"
                )


                # =========================================
                # Why it works
                # =========================================

                why_it_works = recommendation.get(
                    "why_it_works"
                )

                if why_it_works:

                    st.markdown(
                        f"**Why it works:** "
                        f"{why_it_works}"
                    )


                # =========================================
                # Compact Metadata
                # =========================================

                time_horizon = recommendation.get(
                    "time_horizon"
                )

                confidence = recommendation.get(
                    "confidence"
                )

                impacted_metrics = recommendation.get(
                    "impacted_metrics",
                    [],
                )


                metadata = []


                if time_horizon:

                    metadata.append(
                        f"⏱️ **Time:** "
                        f"{str(time_horizon).capitalize()}"
                    )


                if confidence:

                    metadata.append(
                        f"🎯 **Confidence:** "
                        f"{str(confidence).capitalize()}"
                    )


                metadata.append(
                    f"📊 **Metrics:** "
                    f"{len(impacted_metrics)}"
                )


                st.markdown(
                    " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(
                        metadata
                    )
                )


                # =========================================
                # Causal Chain
                # =========================================

                causal_chain = recommendation.get(
                    "causal_chain",
                    [],
                )

                if causal_chain:

                    st.markdown(
                        "**🔗 Causal Chain**"
                    )

                    st.write(
                        " → ".join(
                            str(step)
                            for step in causal_chain
                        )
                    )


                # =========================================
                # Impacted Metrics
                # =========================================

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


                # =========================================
                # Supporting Evidence
                # =========================================

                evidence = recommendation.get(
                    "evidence",
                    [],
                )

                if evidence:

                    st.markdown(
                        "**📖 Supporting Evidence**"
                    )

                    display_evidence(
                        evidence
                    )


                st.divider()


        # =================================================
        # Retrieved Scientific Sources
        # =================================================

        sources = result.get(
            "retrieved_sources",
            [],
        )


        if sources:

            display_sources(
                sources,
                evidence_sources,
            )


        return


    # =====================================================
    # Unknown Response
    # =====================================================

    st.subheader(
        "Response"
    )

    st.json(
        result
    )


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

    st.header(
        "🌍 Environmental Context"
    )

    st.caption(
        "Provide environmental conditions used "
        "by the reasoning pipeline."
    )

    st.divider()


    # =====================================================
    # Soil
    # =====================================================

    st.subheader(
        "🌱 Soil"
    )

    st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1,
        key="soil_ph",
    )

    st.number_input(
        "Soil organic carbon (%)",
        min_value=0.0,
        value=0.3,
        step=0.1,
        key="soil_organic_carbon",
    )

    st.text_input(
        "Soil moisture",
        value="unknown",
        key="soil_moisture",
    )


    # =====================================================
    # Land & Agriculture
    # =====================================================

    st.subheader(
        "🌾 Land & Agriculture"
    )

    st.text_input(
        "Land use type",
        value="monoculture",
        key="land_use_type",
    )

    st.text_input(
        "Crop",
        value="wheat",
        key="crop",
    )

    st.number_input(
        "Species richness",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="species_richness",
    )

    st.number_input(
        "Habitat diversity",
        min_value=0.0,
        value=0.0,
        step=0.1,
        key="habitat_diversity",
    )


    # =====================================================
    # Climate
    # =====================================================

    st.subheader(
        "🌦️ Climate"
    )

    st.number_input(
        "Temperature (°C)",
        value=25.0,
        step=0.5,
        key="temperature",
    )

    st.selectbox(
        "Rainfall",
        [
            "low",
            "medium",
            "high",
        ],
        index=1,
        key="rainfall",
    )

    st.text_input(
        "Region",
        value="semi-arid",
        key="region",
    )


    # =====================================================
    # Environmental Pressure
    # =====================================================

    st.subheader(
        "⚠️ Environmental Pressure"
    )

    st.text_input(
        "Pollution",
        value="",
        key="pollution",
    )

    st.text_input(
        "Deforestation",
        value="",
        key="deforestation",
    )


    # =====================================================
    # Conversation Memory
    # =====================================================

    st.divider()

    st.subheader(
        "🧠 Conversation Memory"
    )

    st.success(
        "Active"
    )

    st.caption(
        "All follow-up questions in this conversation "
        "use the same session."
    )

    if st.button(
        "🔄 Start New Conversation",
        use_container_width=True,
    ):

        start_new_conversation()


# =========================================================
# Existing Chat History
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
# Process New Question
# =========================================================

if question:

    # -----------------------------------------------------
    # Create environmental context
    # -----------------------------------------------------

    metrics = create_metrics()


    # -----------------------------------------------------
    # Display user question
    # -----------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # -----------------------------------------------------
    # Save user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # -----------------------------------------------------
    # Run existing RAG / reasoning pipeline
    # -----------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🔎 Retrieving scientific evidence "
            "and generating recommendations..."
        ):

            try:

                result = process(
                    st.session_state.session_id,
                    metrics,
                    question,
                )


                # -----------------------------------------
                # Display result
                # -----------------------------------------

                display_result(
                    result
                )


                # -----------------------------------------
                # Save assistant response
                # -----------------------------------------

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

                st.exception(
                    e
                )