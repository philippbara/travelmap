from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.services.storage import load_map
from app.config import settings
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    """Render homepage with JSON upload form."""
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get("/map/{map_id}")
def view_map(request: Request, map_id: str):
    """Render the map page with enriched POIs."""
    pois = load_map(map_id)
    return templates.TemplateResponse(
        "map.html",
        {
            "request": request,
            "pois_json": json.dumps([poi.dict() for poi in pois]),
            "mapbox_token": settings.MAPBOX_TOKEN
        }
    )
