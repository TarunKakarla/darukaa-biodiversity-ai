"""
Hand-built environmental causal graph.
Each edge is directional and includes a source. This graph is deliberately
independent of the LLM so recommendations cannot be generated from prompts alone.
"""

EDGES = [
    {"source":"soil_organic_carbon","target":"soil_health","direction":"positive","relation":"higher organic carbon generally supports soil structure, nutrient cycling and biological activity","source_ref":"FAO, Soil organic carbon: the hidden potential"},
    {"source":"soil_moisture","target":"species_survival","direction":"positive","relation":"adequate water availability supports plant productivity and species persistence","source_ref":"IPCC AR6 WGII, terrestrial ecosystems and climate impacts"},
    {"source":"rainfall","target":"soil_moisture","direction":"positive","relation":"rainfall is a major driver of soil water availability, moderated by soil and land cover","source_ref":"IPCC AR6 WGII"},
    {"source":"land_use_type","target":"habitat_diversity","direction":"context_dependent","relation":"diverse land-cover elements can increase habitat heterogeneity compared with simplified monocultures","source_ref":"FAO, Agroforestry for landscape restoration"},
    {"source":"land_use_type","target":"habitat_fragmentation","direction":"negative","relation":"land-use conversion and simplified landscapes can fragment habitats","source_ref":"IPCC AR6 WGII, biodiversity and land-use change"},
    {"source":"habitat_diversity","target":"species_richness","direction":"positive","relation":"greater habitat heterogeneity can provide more niches and resources for species","source_ref":"FAO biodiversity and agroecology resources"},
    {"source":"soil_health","target":"species_richness","direction":"positive","relation":"healthier soils support vegetation and below-ground biological communities that contribute to ecosystem functioning","source_ref":"FAO soil biodiversity resources"},
    {"source":"pollution","target":"species_richness","direction":"negative","relation":"pollution can reduce habitat quality and harm sensitive organisms","source_ref":"IPCC AR6 WGII"},
    {"source":"deforestation","target":"habitat_diversity","direction":"negative","relation":"removal of woody vegetation can reduce habitat structure and connectivity","source_ref":"IPCC AR6 WGII"},
    {"source":"agroforestry","target":"soil_organic_carbon","direction":"positive","relation":"trees and perennial vegetation can add biomass and support carbon accumulation in soils","source_ref":"FAO agroforestry resources"},
    {"source":"cover_crops","target":"soil_organic_carbon","direction":"positive","relation":"continuous plant cover can increase organic inputs and reduce erosion losses","source_ref":"FAO soil and conservation agriculture resources"},
    {"source":"intercropping","target":"habitat_diversity","direction":"positive","relation":"multiple crop species increase crop-system structural and biological diversity","source_ref":"FAO agroecology resources"},
    {"source":"agroforestry","target":"habitat_diversity","direction":"positive","relation":"trees combined with crops create additional vertical and seasonal habitat structure","source_ref":"FAO agroforestry resources"},
    {"source":"agroforestry","target":"soil_moisture","direction":"context_dependent","relation":"tree cover and improved soil structure can alter water infiltration and retention; effects depend on design and climate","source_ref":"FAO agroforestry resources"},
]

CHAINS = [
    ("low_soc", ["soil_organic_carbon","soil_health","species_richness"]),
    ("low_rainfall", ["rainfall","soil_moisture","species_richness"]),
    ("monoculture", ["land_use_type","habitat_diversity","species_richness"]),
    ("land_change", ["land_use_type","habitat_fragmentation","habitat_diversity","species_richness"]),
    ("pollution", ["pollution","species_richness"]),
    ("deforestation", ["deforestation","habitat_diversity","species_richness"]),
]

def relevant_chains(metrics):
    m = metrics.model_dump() if hasattr(metrics, "model_dump") else metrics
    out = []
    if m.get("soil_organic_carbon") is not None and m["soil_organic_carbon"] < 0.6:
        out.append({"name":"soil carbon → soil health → biodiversity","nodes":CHAINS[0][1],"trigger":"soil_organic_carbon < 0.6%","evidence":[EDGES[0],EDGES[6]]})
    if str(m.get("rainfall","")).lower() in {"low","very low","scarce","dry"}:
        out.append({"name":"rainfall → moisture → species persistence","nodes":CHAINS[1][1],"trigger":"low rainfall","evidence":[EDGES[2],EDGES[1]]})
    land = str(m.get("land_use_type","")).lower()
    crop = str(m.get("crop","")).lower()
    if "mono" in land or "wheat" in crop or "mono" in crop:
        out.append({"name":"simplified land use → habitat diversity → richness","nodes":CHAINS[2][1],"trigger":"monoculture/simplified cropping","evidence":[EDGES[3],EDGES[5]]})
    if m.get("pollution"):
        out.append({"name":"pollution → biodiversity pressure","nodes":CHAINS[4][1],"trigger":"pollution reported","evidence":[EDGES[7]]})
    if m.get("deforestation"):
        out.append({"name":"deforestation → habitat diversity → richness","nodes":CHAINS[5][1],"trigger":"deforestation reported","evidence":[EDGES[8],EDGES[5]]})
    return out[:3]

def standalone_test():
    sample = {
        "soil_organic_carbon": 0.3,
        "rainfall": "low",
        "crop": "monoculture wheat",
        "land_use_type": "monoculture",
        "region": "semi-arid"
    }
    return relevant_chains(sample)
