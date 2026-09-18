from app.graph.reasoning_graph import relevant_chains
from app.rag.store import rag_store
from app.llm.client import call_llm
from app.memory.session import merge_metrics, missing_groups
from app.models import EnvironmentalMetrics


QUESTION_MAP = {
    "soil": "soil pH, organic carbon %, or moisture",
    "land_use": "land-use type and crop",
    "climate": "rainfall pattern and temperature",
    "biodiversity": "species richness or habitat diversity",
    "human_impact": "pollution or deforestation level",
}


# Topics/interventions that can be explicitly requested by the user.
INTERVENTION_KEYWORDS = {
    "agroforestry": [
        "agroforestry",
        "agro-forestry",
        "trees in farms",
        "trees on farms",
        "farm trees",
    ],
    "conservation_agriculture": [
        "conservation agriculture",
        "minimum tillage",
        "no tillage",
        "zero tillage",
        "soil cover",
    ],
    "crop_diversification": [
        "crop diversification",
        "crop rotation",
        "intercropping",
        "mixed cropping",
        "legume rotation",
    ],
    "habitat_diversity": [
        "habitat diversity",
        "habitat heterogeneity",
        "habitat complexity",
    ],
    "soil_health": [
        "soil health",
        "soil organic carbon",
        "organic carbon",
        "soil moisture",
        "soil degradation",
    ],
    "pollution": [
        "pollution",
        "pesticide pollution",
        "chemical pollution",
        "agricultural pollution",
    ],
}


def detect_requested_intervention(message):
    """
    Detect whether the user explicitly asks about a particular
    intervention or environmental topic.

    Returns the canonical topic name or None.
    """

    if not message:
        return None

    text = message.lower()

    # Check longer/more specific phrases first.
    matches = []

    for topic, keywords in INTERVENTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                matches.append(
                    (len(keyword), topic)
                )

    if not matches:
        return None

    # Prefer the longest matching phrase.
    matches.sort(reverse=True)

    return matches[0][1]


def process(session_id, metrics: EnvironmentalMetrics, message=None):

    # ---------------------------------------------------------
    # 1. Merge current metrics with session memory
    # ---------------------------------------------------------

    state = merge_metrics(session_id, metrics)

    # ---------------------------------------------------------
    # 2. Ask for missing environmental information
    # ---------------------------------------------------------

    missing = missing_groups(state)

    if missing:
        ask = ", ".join(
            QUESTION_MAP[x]
            for x in missing[:2]
        )

        return {
            "type": "clarification",
            "question": (
                "To reason without guessing, can you provide "
                f"{ask}?"
            ),
            "missing_metrics": missing,
        }

    # ---------------------------------------------------------
    # 3. Detect what the user is specifically asking about
    # ---------------------------------------------------------

    requested_intervention = detect_requested_intervention(
        message
    )

    # ---------------------------------------------------------
    # 4. Build causal chains
    # ---------------------------------------------------------

    chains = relevant_chains(state)

    # ---------------------------------------------------------
    # 5. Build RAG query
    #
    # If the user explicitly asks about something such as
    # agroforestry, make that topic dominant in retrieval.
    # ---------------------------------------------------------

    query_parts = []

    if message:
        query_parts.append(message)

    if requested_intervention:
        query_parts.append(
            f"Specific intervention: {requested_intervention}"
        )

    query_parts.append(str(state))

    if chains:
        query_parts.append(
            " ".join(
                chain["name"]
                for chain in chains
            )
        )

    query = " ".join(query_parts)

    # ---------------------------------------------------------
    # 6. Retrieve scientific evidence
    # ---------------------------------------------------------

    retrieved = rag_store.retrieve(
        query,
        5
    )

    # ---------------------------------------------------------
    # 7. Ask the LLM to answer the question specifically
    # ---------------------------------------------------------

    result = call_llm(
        state,
        chains,
        retrieved,
        user_question=message,
        requested_intervention=requested_intervention,
    )

    # ---------------------------------------------------------
    # 8. Normalize unexpected LLM output
    # ---------------------------------------------------------

    if isinstance(result, list):
        result = {
            "summary": "",
            "recommendations": result,
        }

    if not isinstance(result, dict):
        result = {
            "summary": "",
            "recommendations": [],
        }

    # ---------------------------------------------------------
    # 9. Attach retrieved sources
    # ---------------------------------------------------------

    result["type"] = "recommendations"

    result["retrieved_sources"] = [
        x["metadata"]
        for x in retrieved
    ]

    return result