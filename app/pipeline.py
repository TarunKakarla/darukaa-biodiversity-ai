from typing import Any, Dict, Optional

from app.graph.reasoning_graph import relevant_chains, analyze_multi_metric_nexus
from app.rag.store import rag_store
from app.llm.client import call_llm
from app.memory.session import (
    merge_metrics,
    missing_groups,
    add_turn,
    get_conversation_history,
    get_session_summary
)
from app.models import EnvironmentalMetrics


QUESTION_MAP = {
    "soil": "soil organic carbon %, soil pH, or moisture level",
    "land_use": "land-use type (e.g. monoculture, pasture) and current crop",
    "climate": "rainfall pattern (low/medium/high) and temperature or region",
    "biodiversity": "species richness or habitat diversity indicators",
    "human_impact": "pollution level or deforestation impact",
}

INTERVENTION_KEYWORDS = {
    "agroforestry": [
        "agroforestry",
        "agro-forestry",
        "trees in farms",
        "trees on farms",
        "farm trees",
        "silvopasture",
        "windbreaks",
        "hedgerows"
    ],
    "conservation_agriculture": [
        "conservation agriculture",
        "minimum tillage",
        "no tillage",
        "zero tillage",
        "soil cover",
        "mulching",
        "residue retention"
    ],
    "crop_diversification": [
        "crop diversification",
        "crop rotation",
        "intercropping",
        "mixed cropping",
        "legume rotation",
        "polyculture",
        "companion planting"
    ],
    "habitat_diversity": [
        "habitat diversity",
        "habitat heterogeneity",
        "habitat complexity",
        "ecological corridors",
        "pollinator strips"
    ],
    "soil_health": [
        "soil health",
        "soil organic carbon",
        "organic carbon",
        "soil moisture",
        "soil degradation",
        "soil ph"
    ],
    "pollution": [
        "pollution",
        "pesticide pollution",
        "chemical pollution",
        "agricultural pollution",
        "runoff"
    ],
}


def detect_requested_intervention(message: Optional[str]) -> Optional[str]:
    """
    Detects whether the user explicitly asks about a particular intervention
    or environmental topic.
    """
    if not message:
        return None

    text = message.lower()
    matches = []

    for topic, keywords in INTERVENTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                matches.append((len(keyword), topic))

    if not matches:
        return None

    matches.sort(reverse=True)
    return matches[0][1]


def process(
    session_id: str,
    metrics: Optional[EnvironmentalMetrics] = None,
    message: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main reasoning pipeline connecting:
    1. Session memory & conversational parameter extraction
    2. Incomplete input detection & scientific clarifying questions
    3. Multi-metric nexus coupling (at least 3 environmental variables)
    4. Causal reasoning graph execution
    5. Hybrid RAG retrieval (authoritative FAO/IPCC/CBD/IPBES literature)
    6. LLM / Autonomous Scientific Reasoning Engine
    7. Multi-turn conversation state persistence
    """
    # ---------------------------------------------------------
    # 1. Merge metrics with session memory + parse message text
    # ---------------------------------------------------------
    state = merge_metrics(session_id, metrics, user_message=message)

    # ---------------------------------------------------------
    # 2. Check for incomplete input requiring clarification
    # ---------------------------------------------------------
    # In order to perform multi-variable reasoning without guessing,
    # the system needs at least 3 distinct environmental dimensions.
    missing = missing_groups(state)
    present_groups_count = 5 - len(missing)

    # Check if the user is asking an initial high-level question without sufficient parameters
    is_initial_vague_query = False
    if message:
        m_lower = message.lower()
        if any(phrase in m_lower for phrase in [
            "biodiversity is declining",
            "restore my land",
            "improve biodiversity",
            "soil is degrading",
            "wildlife is disappearing",
            "what can i do"
        ]) and present_groups_count < 3:
            is_initial_vague_query = True

    if is_initial_vague_query or present_groups_count < 2:
        # Formulate clarifying question specifying missing variables (as in the hackathon brief)
        needed_labels = [QUESTION_MAP[x] for x in missing[:3] if x in QUESTION_MAP]
        ask_text = ", ".join(needed_labels)

        clarification_response = {
            "type": "clarification",
            "question": f"To evaluate your ecosystem without guessing, can you provide {ask_text}?",
            "missing_metrics": missing,
            "session_id": session_id,
            "current_state": state
        }
        add_turn(session_id, message or "", clarification_response)
        return clarification_response

    # ---------------------------------------------------------
    # 3. Detect requested topic / intervention
    # ---------------------------------------------------------
    requested_intervention = detect_requested_intervention(message)

    # ---------------------------------------------------------
    # 4. Multi-Metric Nexus Coupling (At least 3 variables)
    # ---------------------------------------------------------
    nexus = analyze_multi_metric_nexus(state)

    # ---------------------------------------------------------
    # 5. Build Causal Reasoning Pathways
    # ---------------------------------------------------------
    chains = relevant_chains(state)

    # ---------------------------------------------------------
    # 6. Retrieve Hybrid Scientific Evidence (RAG)
    # ---------------------------------------------------------
    query_parts = []
    if message:
        query_parts.append(message)
    if requested_intervention:
        query_parts.append(f"intervention: {requested_intervention}")

    # Add environmental context terms to RAG query
    if state.get("soil_organic_carbon"):
        query_parts.append(f"soil organic carbon {state['soil_organic_carbon']}%")
    if state.get("rainfall"):
        query_parts.append(f"rainfall {state['rainfall']}")
    if state.get("crop"):
        query_parts.append(f"crop {state['crop']}")
    if state.get("region"):
        query_parts.append(f"region {state['region']}")

    query = " ".join(query_parts)
    retrieved = rag_store.retrieve(query, k=5)

    # ---------------------------------------------------------
    # 7. Retrieve Multi-Turn Conversation History
    # ---------------------------------------------------------
    history = get_conversation_history(session_id, last_n=4)

    # ---------------------------------------------------------
    # 8. Call LLM or Autonomous Scientific Synthesis Engine
    # ---------------------------------------------------------
    result = call_llm(
        state,
        chains,
        retrieved,
        user_question=message,
        requested_intervention=requested_intervention,
        conversation_history=history,
        multi_metric_nexus=nexus,
        override_api_key=api_key,
        override_base_url=base_url,
        override_model=model_name,
    )

    # ---------------------------------------------------------
    # 9. Normalize & Attach Scientific Metadata
    # ---------------------------------------------------------
    if isinstance(result, list):
        result = {
            "summary": "",
            "recommendations": result,
        }
    elif not isinstance(result, dict):
        result = {
            "summary": "",
            "recommendations": [],
        }

    result["type"] = "recommendations"
    result["multi_metric_nexus"] = nexus
    result["retrieved_sources"] = [x.get("metadata", {}) for x in retrieved]
    result["session_id"] = session_id

    # ---------------------------------------------------------
    # 10. Record Conversation Memory Turn
    # ---------------------------------------------------------
    add_turn(session_id, message or "Environmental Assessment", result)

    summary_info = get_session_summary(session_id)
    result["session_turn"] = summary_info["total_turns"]

    return result