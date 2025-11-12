from pydantic import BaseModel

class POI(BaseModel):
    name: str
    lat: float
    lon: float
    place_name: str
