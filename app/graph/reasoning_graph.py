"""
Comprehensive Ecological Causal Reasoning Graph & Multi-Metric Nexus Engine.
Implements multi-variable ecological coupling connecting:
1. Soil Health ↔ 2. Climate/Water Dynamics ↔ 3. Land Use / Habitat Fragmentation ↔ 4. Biodiversity ↔ 5. Human Pressure
Deliberately structured to evaluate at least 3 environmental variables together.
"""

from typing import Any, Dict, List, Optional


ECOLOGICAL_EDGES = [
    # Soil Health Dynamics
    {
        "source": "soil_organic_carbon",
        "target": "soil_health",
        "direction": "positive",
        "relation": "Higher SOC enhances microbial biomass, aggregate stability, and nutrient cycling efficiency.",
        "source_ref": "FAO, Soil organic carbon: the hidden potential (2019)"
    },
    {
        "source": "soil_organic_carbon",
        "target": "soil_moisture",
        "direction": "positive",
        "relation": "Each 1% increase in SOC can hold up to 150,000 liters of additional water per hectare.",
        "source_ref": "IPCC Special Report on Climate Change and Land (2019)"
    },
    {
        "source": "soil_ph",
        "target": "soil_health",
        "direction": "optimal_window",
        "relation": "Soil pH outside 6.0-7.5 severely restricts phosphorus availability and mycorrhizal colonization.",
        "source_ref": "FAO Global Soil Partnership Technical Report"
    },

    # Water & Climate Coupling
    {
        "source": "rainfall",
        "target": "soil_moisture",
        "direction": "positive",
        "relation": "Rainfall governs soil moisture replenishing rate, strongly moderated by infiltration capacity and organic mulch.",
        "source_ref": "IPCC AR6 WGII Chapter 4"
    },
    {
        "source": "temperature",
        "target": "soil_moisture",
        "direction": "negative",
        "relation": "Elevated temperatures accelerate evapotranspiration and deplete root-zone available water.",
        "source_ref": "IPCC AR6 WGII"
    },
    {
        "source": "soil_moisture",
        "target": "species_survival",
        "direction": "positive",
        "relation": "Adequate soil water availability prevents drought-induced plant mortality and sustains subterranean invertebrate activity.",
        "source_ref": "CBD Global Biodiversity Outlook 5"
    },

    # Land Cover & Fragmentation
    {
        "source": "land_use_type",
        "target": "habitat_diversity",
        "direction": "context_dependent",
        "relation": "Transition from simplified monocultures to polycultures introduces ecological niches and structural vertical strata.",
        "source_ref": "FAO State of the World's Biodiversity (2019)"
    },
    {
        "source": "monoculture",
        "target": "habitat_fragmentation",
        "direction": "positive",
        "relation": "Extensive single-crop regimes fragment native vegetative corridors, isolating wild pollinator and insect populations.",
        "source_ref": "IPBES Global Assessment Report"
    },
    {
        "source": "habitat_diversity",
        "target": "species_richness",
        "direction": "positive",
        "relation": "Heterogeneous canopies and diverse vegetation provide continuous floral nectar, overwintering refugia, and prey.",
        "source_ref": "FAO, Agroforestry for landscape restoration"
    },

    # Human Impact & Stressors
    {
        "source": "pollution",
        "target": "species_richness",
        "direction": "negative",
        "relation": "Agrochemical runoff and synthetic pesticides reduce non-target soil invertebrates and wild pollinators.",
        "source_ref": "IPBES Global Assessment Report"
    },
    {
        "source": "deforestation",
        "target": "habitat_diversity",
        "direction": "negative",
        "relation": "Canopy removal destroys microclimatic buffers and causes rapid oxidation of surface organic carbon.",
        "source_ref": "IPCC AR6 WGII"
    },

    # Ecological Interventions
    {
        "source": "agroforestry",
        "target": "soil_organic_carbon",
        "direction": "positive",
        "relation": "Deep tree roots deposit recalcitrant carbon at depth and provide continuous leaf litter mulching.",
        "source_ref": "FAO State of the World's Biodiversity (2019)"
    },
    {
        "source": "agroforestry",
        "target": "habitat_diversity",
        "direction": "positive",
        "relation": "Multi-strata canopy creates diverse thermal and structural micro-habitats for birds and pollinators.",
        "source_ref": "FAO Agroforestry guidelines"
    },
    {
        "source": "legume_cover_crops",
        "target": "soil_organic_carbon",
        "direction": "positive",
        "relation": "Biological nitrogen fixation stimulates microbial decomposition of crop residues into stable humic fractions.",
        "source_ref": "FAO, Soil organic carbon: the hidden potential"
    },
    {
        "source": "intercropping",
        "target": "species_richness",
        "direction": "positive",
        "relation": "Crop polycultures disrupt pest cycles and supply diverse pollen resources throughout the growing season.",
        "source_ref": "CBD Global Biodiversity Outlook 5"
    }
]


def analyze_multi_metric_nexus(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates cross-coupling across at least 3 environmental variables simultaneously.
    Identifies systemic vulnerabilities, feedback loops, and synergistic interventions.
    """
    soc = metrics.get("soil_organic_carbon")
    rainfall = str(metrics.get("rainfall", "")).lower()
    crop = str(metrics.get("crop", "")).lower()
    land_use = str(metrics.get("land_use_type", "")).lower()
    region = str(metrics.get("region", "")).lower()
    ph = metrics.get("soil_ph")
    temp = metrics.get("temperature")
    pollution = metrics.get("pollution")

    coupled_variables = []
    nexus_name = "Ecological Baseline Assessment"
    compound_risk = "Moderate"
    mechanisms = []
    recommended_interventions = []

    # Check Variable 1: Soil Carbon & Health
    if soc is not None:
        coupled_variables.append(f"Soil Organic Carbon ({soc}%)")
        if soc < 0.6:
            mechanisms.append("Severe soil organic carbon deficit (<0.6%) impairs aggregate stability and microbial respiration.")
        else:
            mechanisms.append(f"Soil organic carbon maintained at {soc}%.")

    # Check Variable 2: Climate / Moisture Dynamics
    if rainfall in ["low", "scarce", "dry", "very low"] or "semi-arid" in region or "arid" in region:
        coupled_variables.append("Climate: Low Rainfall / Aridity Stress")
        mechanisms.append("Low rainfall restricts soil water replenishment; unmulched bare soil experiences excessive evaporation.")
    elif rainfall in ["medium", "high"]:
        coupled_variables.append(f"Climate: {rainfall.capitalize()} Rainfall")

    # Check Variable 3: Land Cover / Monoculture Fragmentation
    if "mono" in land_use or "wheat" in crop or "mono" in crop or "crop" in land_use:
        coupled_variables.append(f"Land Use: Simplified Cropping ({crop or 'Monoculture'})")
        mechanisms.append("Monoculture canopy creates structural homogeneity, leaving pollinators without floral nectar corridors.")

    # Check Variable 4: Chemical Pressure / Temperature
    if pollution and str(pollution).lower() not in ["none", "", "low"]:
        coupled_variables.append(f"Human Impact: {pollution}")
        mechanisms.append("Agrochemical pressure suppresses beneficial predatory arthropods and soil mycorrhizal networks.")

    # Multi-Variable Triple Nexus Synthesis
    if len(coupled_variables) >= 3:
        if (soc is not None and soc < 0.6) and (rainfall in ["low", "dry"] or "semi-arid" in region) and ("mono" in land_use or "wheat" in crop):
            nexus_name = "Compound Arid-Monoculture Degradation Loop"
            compound_risk = "Critical (Compounded Soil-Water-Biodiversity Stress)"
            recommended_interventions = [
                "Agroforestry (Windbreak & N-fixing Faidherbia/Acacia hedgerows)",
                "Legume-cereal intercropping (e.g. Wheat + Chickpea/Lentil)",
                "Conservation tillage with surface residue mulch retention"
            ]
        else:
            nexus_name = "Coupled Landscape-Soil-Biodiversity Nexus"
            compound_risk = "Moderate to High"
            recommended_interventions = [
                "Agroecological diversification & border floral strips",
                "Organic soil amendments & cover cropping"
            ]

    return {
        "nexus_name": nexus_name,
        "coupled_variables": coupled_variables,
        "variable_count": len(coupled_variables),
        "compound_risk": compound_risk,
        "ecological_mechanisms": mechanisms,
        "recommended_interventions": recommended_interventions,
        "satisfies_multi_variable_constraint": len(coupled_variables) >= 3
    }


def relevant_chains(metrics: Any) -> List[Dict[str, Any]]:
    """
    Constructs directional causal pathways connecting environmental drivers to biodiversity outcomes.
    """
    m = metrics.model_dump() if hasattr(metrics, "model_dump") else metrics
    chains = []

    soc = m.get("soil_organic_carbon")
    rainfall = str(m.get("rainfall", "")).lower()
    land = str(m.get("land_use_type", "")).lower()
    crop = str(m.get("crop", "")).lower()
    region = str(m.get("region", "")).lower()

    # Chain 1: Soil Carbon -> Water Holding -> Soil Biodiversity
    if soc is not None and soc < 0.8:
        chains.append({
            "name": "soil carbon → soil health → subterranean biodiversity",
            "nodes": ["soil_organic_carbon", "aggregate_stability", "microbial_biomass", "species_richness"],
            "trigger": f"Soil organic carbon is {soc}% (< 0.8% threshold)",
            "causal_explanation": "Low SOC reduces organic matter substrates, limiting earthworm, fungal, and bacterial activity.",
            "source_ref": "FAO, Soil organic carbon: the hidden potential (2019)"
        })

    # Chain 2: Low Rainfall -> Soil Moisture -> Drought Vulnerability
    if rainfall in ["low", "very low", "scarce", "dry"] or "semi-arid" in region:
        chains.append({
            "name": "rainfall → moisture → species persistence",
            "nodes": ["rainfall", "soil_moisture", "primary_productivity", "species_survival"],
            "trigger": "Low rainfall / Semi-arid hydrological regime",
            "causal_explanation": "Water-limited systems require organic ground cover and microclimatic tree buffers to prevent plant desiccation.",
            "source_ref": "IPCC AR6 WGII Chapter 4 & SRCCL"
        })

    # Chain 3: Monoculture -> Structural Homogeneity -> Pollinator Deficit
    if "mono" in land or "wheat" in crop or "mono" in crop:
        chains.append({
            "name": "simplified land use → habitat diversity → species richness",
            "nodes": ["land_use_type", "habitat_fragmentation", "habitat_diversity", "species_richness"],
            "trigger": f"Simplified agricultural landscape ({crop or 'monoculture'})",
            "causal_explanation": "Single-species crop canopies lack continuous flowering resources and overwintering structural shelter.",
            "source_ref": "CBD Global Biodiversity Outlook 5 & FAO State of World's Biodiversity"
        })

    # Chain 4: Chemical / Pollution Pressures
    if m.get("pollution"):
        chains.append({
            "name": "Agrochemical Pollution → Non-Target Arthropod Mortality → Food Web Collapse",
            "nodes": ["pollution", "soil_microbiome", "beneficial_predators", "species_richness"],
            "trigger": f"Chemical pollution detected ({m.get('pollution')})",
            "causal_explanation": "Ecotoxic pesticide exposure reduces natural biological control agents and aquatic macroinvertebrates.",
            "source_ref": "IPBES Global Assessment Report"
        })

    return chains[:4]
