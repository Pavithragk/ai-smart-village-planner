from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class VillageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    district: Optional[str] = None
    state: Optional[str] = "Karnataka"
    population: int = Field(..., gt=0)
    area_hectares: float = Field(..., gt=0)
    rainfall_mm: float = Field(..., ge=0)
    water_sources: int = Field(0, ge=0)
    num_schools: int = Field(0, ge=0)
    num_health_centers: int = Field(0, ge=0)
    primary_crops: Optional[str] = None
    soil_type: Optional[str] = "loamy"
    budget_lakhs: float = Field(0, ge=0)
    electricity: bool = True
    road_connectivity: bool = True

class VillageResponse(BaseModel):
    id: int
    name: str
    district: Optional[str]
    state: Optional[str]
    population: int
    area_hectares: float
    rainfall_mm: float
    water_sources: int
    num_schools: int
    num_health_centers: int
    primary_crops: Optional[str]
    soil_type: Optional[str]
    budget_lakhs: float
    electricity: bool
    road_connectivity: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AnalysisMetric(BaseModel):
    label: str
    value: str
    status: str
    detail: str

class AnalysisResponse(BaseModel):
    village_id: int
    village_name: str
    metrics: List[AnalysisMetric]
    overall_status: str

class RecommendationItem(BaseModel):
    module: str
    priority: str
    title: str
    content: str
    cost_lakhs: float