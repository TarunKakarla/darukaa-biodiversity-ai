from collections import defaultdict

SESSIONS = defaultdict(dict)

REQUIRED_GROUPS = {
    "soil": ["soil_ph","soil_organic_carbon","soil_moisture"],
    "land_use": ["land_use_type","crop"],
    "climate": ["temperature","rainfall"],
    "biodiversity": ["species_richness","habitat_diversity"],
    "human_impact": ["pollution","deforestation"],
}

def merge_metrics(session_id, new_metrics):
    state = SESSIONS[session_id]
    incoming = new_metrics.model_dump(exclude_none=True) if hasattr(new_metrics,"model_dump") else {k:v for k,v in new_metrics.items() if v is not None}
    state.update(incoming)
    return state

def missing_groups(metrics):
    missing = []
    for group, keys in REQUIRED_GROUPS.items():
        if not any(metrics.get(k) is not None for k in keys):
            missing.append(group)
    return missing
