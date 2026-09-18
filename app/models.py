from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

class EnvironmentalMetrics(BaseModel):
    soil_ph: Optional[float] = None
    soil_organic_carbon: Optional[float] = None
    soil_moisture: Optional[str] = None
    land_use_type: Optional[str] = None
    crop: Optional[str] = None
    species_richness: Optional[float] = None
    habitat_diversity: Optional[float] = None
    temperature: Optional[float] = None
    rainfall: Optional[str] = None
    pollution: Optional[str] = None
    deforestation: Optional[str] = None
    region: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str = "default"
    message: Optional[str] = None
    metrics: Optional[EnvironmentalMetrics] = None

class ClarifyingResponse(BaseModel):
    type: Literal["clarification"]
    question: str
    missing_metrics: List[str]

class Recommendation(BaseModel):
    what_to_do: str
    why_it_works: str
    causal_chain: List[str]
    impacted_metrics: List[str]
    time_horizon: Literal["short", "medium", "long"]
    confidence: Literal["low", "medium", "high"]
    evidence: List[Dict[str, Any]]

class ScientistResponse(BaseModel):
    type: Literal["recommendations"]
    summary: str
    recommendations: List[Recommendation]
    retrieved_sources: List[Dict[str, Any]]
