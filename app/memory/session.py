import re
from collections import defaultdict
from typing import Any, Dict, List, Optional

# In-memory storage for active sessions
SESSIONS = defaultdict(dict)
SESSION_HISTORIES = defaultdict(list)
SESSION_METADATA = defaultdict(dict)

REQUIRED_GROUPS = {
    "soil": ["soil_ph", "soil_organic_carbon", "soil_moisture"],
    "land_use": ["land_use_type", "crop"],
    "climate": ["temperature", "rainfall", "region"],
    "biodiversity": ["species_richness", "habitat_diversity"],
    "human_impact": ["pollution", "deforestation", "pesticide_use"],
}


def extract_metrics_from_text(text: str) -> Dict[str, Any]:
    """
    Intelligently extracts environmental parameters directly from natural language chat messages.
    Supports conversational inputs such as:
    'My soil carbon is 0.3%, rainfall is low, crop is monoculture wheat in a semi-arid zone'
    """
    if not text:
        return {}

    extracted = {}
    lower = text.lower()

    # Soil Organic Carbon (%)
    soc_match = re.search(
        r"(?:soc|organic carbon|soil organic carbon|carbon)\s*(?:is|of|level|:|=|\bat\b)?\s*([0-9]+(?:\.[0-9]+)?)\s*%",
        lower
    )
    if not soc_match:
        soc_match = re.search(
            r"([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:soc|organic carbon|soil carbon)",
            lower
        )
    if soc_match:
        try:
            extracted["soil_organic_carbon"] = float(soc_match.group(1))
        except ValueError:
            pass

    # Soil pH
    ph_match = re.search(
        r"(?:ph|soil ph)\s*(?:is|of|:|=|\bat\b)?\s*([0-9]+(?:\.[0-9]+)?)",
        lower
    )
    if ph_match:
        try:
            val = float(ph_match.group(1))
            if 0.0 <= val <= 14.0:
                extracted["soil_ph"] = val
        except ValueError:
            pass

    # Temperature (°C)
    temp_match = re.search(
        r"([0-9]+(?:\.[0-9]+)?)\s*(?:°\s*c|celsius|degrees c|deg c)",
        lower
    )
    if not temp_match:
        temp_match = re.search(
            r"(?:temperature|temp)\s*(?:is|of|:|=|\bat\b)?\s*([0-9]+(?:\.[0-9]+)?)",
            lower
        )
    if temp_match:
        try:
            extracted["temperature"] = float(temp_match.group(1))
        except ValueError:
            pass

    # Rainfall pattern
    if any(k in lower for k in ["low rainfall", "scarce rain", "dry rainfall", "rainfall is low", "drought prone"]):
        extracted["rainfall"] = "low"
    elif any(k in lower for k in ["high rainfall", "heavy rain", "abundant rainfall", "rainfall is high"]):
        extracted["rainfall"] = "high"
    elif any(k in lower for k in ["moderate rainfall", "medium rainfall", "average rainfall"]):
        extracted["rainfall"] = "medium"

    # Region / Climate zone
    if "semi-arid" in lower or "semi arid" in lower:
        extracted["region"] = "semi-arid"
    elif "arid" in lower:
        extracted["region"] = "arid"
    elif "mediterranean" in lower:
        extracted["region"] = "mediterranean"
    elif "tropical" in lower:
        extracted["region"] = "tropical"
    elif "temperate" in lower:
        extracted["region"] = "temperate"

    # Land use & Crop
    if "monoculture" in lower:
        extracted["land_use_type"] = "monoculture"
    elif "agroforestry" in lower:
        extracted["land_use_type"] = "agroforestry"
    elif "intercropping" in lower or "intercropped" in lower:
        extracted["land_use_type"] = "intercropping"
    elif "cropland" in lower or "farmland" in lower or "arable" in lower:
        extracted["land_use_type"] = "cropland"

    for crop_name in ["wheat", "corn", "maize", "soybean", "soy", "rice", "barley", "cotton", "sorghum", "millet"]:
        if crop_name in lower:
            extracted["crop"] = crop_name
            break

    # Biodiversity indicators
    richness_match = re.search(
        r"(?:species richness|richness|species count)\s*(?:is|of|:|=|\bat\b)?\s*([0-9]+)",
        lower
    )
    if richness_match:
        try:
            extracted["species_richness"] = float(richness_match.group(1))
        except ValueError:
            pass

    # Human impacts
    if "pesticide" in lower or "chemical" in lower or "fertilizer runoff" in lower:
        extracted["pollution"] = "chemical/pesticide"
    elif "organic farm" in lower or "no pesticides" in lower or "chemical-free" in lower:
        extracted["pollution"] = "none"

    if "deforested" in lower or "deforestation" in lower or "cleared land" in lower:
        extracted["deforestation"] = "moderate/high"

    return extracted


def merge_metrics(session_id: str, new_metrics: Any, user_message: Optional[str] = None) -> Dict[str, Any]:
    """
    Merges incoming EnvironmentalMetrics, natural language extracted metrics,
    and accumulated state for a session.
    """
    state = SESSIONS[session_id]

    # 1. Merge structured incoming metrics
    if hasattr(new_metrics, "model_dump"):
        incoming = new_metrics.model_dump(exclude_none=True)
    elif isinstance(new_metrics, dict):
        incoming = {k: v for k, v in new_metrics.items() if v is not None}
    else:
        incoming = {}

    state.update(incoming)

    # 2. Extract metrics from message text if available and merge
    if user_message:
        text_metrics = extract_metrics_from_text(user_message)
        state.update(text_metrics)

    return state


def add_turn(
    session_id: str,
    user_message: str,
    assistant_response: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Records a completed conversational turn in the session memory.
    """
    history = SESSION_HISTORIES[session_id]
    turn_record = {
        "turn": len(history) + 1,
        "user_message": user_message,
        "assistant_response": assistant_response,
        "metadata": metadata or {}
    }
    history.append(turn_record)


def get_conversation_history(session_id: str, last_n: int = 4) -> List[Dict[str, Any]]:
    """
    Returns recent dialogue turns for prompt context and multi-turn reasoning.
    """
    return SESSION_HISTORIES[session_id][-last_n:]


def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Provides a comprehensive snapshot of what the AI scientist remembers about this session.
    """
    state = SESSIONS.get(session_id, {})
    history = SESSION_HISTORIES.get(session_id, [])

    topics_discussed = []
    prior_recommendations = []

    for turn in history:
        resp = turn.get("assistant_response", {})
        if isinstance(resp, dict):
            for rec in resp.get("recommendations", []):
                if isinstance(rec, dict) and rec.get("what_to_do"):
                    prior_recommendations.append(rec["what_to_do"])

    return {
        "session_id": session_id,
        "total_turns": len(history),
        "environmental_state": state,
        "prior_recommendations": list(dict.fromkeys(prior_recommendations)),
        "is_active": len(history) > 0 or len(state) > 0
    }


def reset_session(session_id: str):
    """
    Clears all state and conversational memory for a specific session.
    """
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    if session_id in SESSION_HISTORIES:
        del SESSION_HISTORIES[session_id]
    if session_id in SESSION_METADATA:
        del SESSION_METADATA[session_id]


def missing_groups(metrics: Dict[str, Any]) -> List[str]:
    """
    Identifies which critical environmental dimensions are missing.
    Requires at least 3 distinct environmental dimensions for multi-metric reasoning.
    """
    missing = []
    for group, keys in REQUIRED_GROUPS.items():
        has_any = any(metrics.get(k) is not None for k in keys)
        if not has_any:
            missing.append(group)
    return missing
