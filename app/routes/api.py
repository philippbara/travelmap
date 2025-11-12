from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.poi_enrichment import enrich_pois
from app.services.storage import save_map
from app.models.poi import POI

router = APIRouter(prefix="/api")

@router.post("/generate")
def generate_map(pois_text: list[dict]):
    """Accept text-only POIs, enrich them, save map, return map_id."""
    enriched = enrich_pois(pois_text)
    map_id = save_map(enriched)
    return JSONResponse({"map_id": map_id, "count": len(enriched)})
