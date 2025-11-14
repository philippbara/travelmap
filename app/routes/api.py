from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.poi import POI
from app.services.storage import save_map
from app.services.poi_enrichment import enrich_pois, parse_blog_to_pois

router = APIRouter(prefix="/api")


@router.post("/generate")
async def generate_map(pois_text: list[dict]):
    """Accept text-only POIs, enrich them, save map, return map_id."""
    enriched = enrich_pois(pois_text)
    map_id = save_map(enriched)
    return JSONResponse({"map_id": map_id, "count": len(enriched)})


@router.post("/llm_parse")
async def llm_parse(blog_data: dict):
    """
    Accepts {"url": "..."}.
    Uses LLM (or mock function for MVP) to extract POIs from blog content.
    Saves the enriched map and returns map_id.
    """
    url = blog_data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' in request")

    pois_json = await parse_blog_to_pois(url)  # returns list[dict] with {"name": ...}
    enriched = enrich_pois(pois_json)
    map_id = save_map(enriched)

    return JSONResponse({"map_id": map_id, "count": len(enriched)})
