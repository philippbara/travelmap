from pydantic import BaseModel
from typing import List, Literal

class FeatureProperties(BaseModel):
    order: int
    name: str
    category: str  # Can eventually be restricted to your ENUM
    country_code: str
    description: str
    link: str

class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    properties: FeatureProperties

class MapJson(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    properties: dict  # title, description
    features: List[Feature]
