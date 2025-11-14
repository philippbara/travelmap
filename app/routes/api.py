from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.storage import save_map
from app.services.poi_enrichment import enrich_pois, parse_blog_to_pois

router = APIRouter(prefix="/api")


@router.post("/generate")
async def generate_map(map_json: dict):
    """
    Accept a FeatureCollection JSON from the LLM,
    enrich features with coordinates, save the map,
    and return map_id.
    """
    try:
        features = map_json.get("features", [])
        if not features:
            raise HTTPException(status_code=400, detail="No features found in input JSON.")

        enriched_features = enrich_pois(features)
        map_json["features"] = enriched_features

        map_id = save_map(map_json)
        return JSONResponse({"map_id": map_id, "count": len(enriched_features)})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

    pois_dict = await parse_blog_to_pois(url)  # returns list[dict] with {"name": ...}
    enriched = enrich_pois(pois_dict)
    map_id = save_map(enriched)

    return JSONResponse({"map_id": map_id, "count": len(enriched)})
