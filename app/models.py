from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class EnvironmentalMetrics(BaseModel):
    # Soil Health
    soil_ph: Optional[float] = None
    soil_organic_carbon: Optional[float] = None
    soil_moisture: Optional[str] = None
    bulk_density: Optional[float] = None

    # Land Use / Cover
    land_use_type: Optional[str] = None
    crop: Optional[str] = None
    canopy_cover: Optional[float] = None

    # Biodiversity Indicators
    species_richness: Optional[float] = None
    habitat_diversity: Optional[float] = None
    pollinator_density: Optional[str] = None

    # Climate Factors
    temperature: Optional[float] = None
    rainfall: Optional[str] = None
    aridity_index: Optional[str] = None
    region: Optional[str] = None

    # Human Impact
    pollution: Optional[str] = None
    deforestation: Optional[str] = None
    pesticide_use: Optional[str] = None

    # Spatial Context / Coordinates (Bonus Feature)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ecoregion: Optional[str] = None
    biome: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str = "default"
    message: Optional[str] = None
    metrics: Optional[EnvironmentalMetrics] = None


class ClarifyingResponse(BaseModel):
    type: Literal["clarification"] = "clarification"
    question: str
    missing_metrics: List[str]
    suggested_inputs: Optional[List[str]] = None


class Recommendation(BaseModel):
    what_to_do: str
    why_it_works: str
    causal_chain: List[str]
    impacted_metrics: List[str]
    time_horizon: Literal["short", "medium", "long"]
    confidence: Literal["low", "medium", "high"]
    measurable_impact: Optional[str] = None
    trade_offs_or_prerequisites: Optional[str] = None
    evidence: List[Dict[str, Any]] = Field(default_factory=list)


class ScientistResponse(BaseModel):
    type: Literal["recommendations"] = "recommendations"
    summary: str
    multi_metric_nexus: Optional[Dict[str, Any]] = None
    recommendations: List[Recommendation]
    retrieved_sources: List[Dict[str, Any]] = Field(default_factory=list)
    session_turn: Optional[int] = None
    spatial_summary: Optional[str] = None

