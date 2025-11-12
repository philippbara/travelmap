import requests
from app.models.poi import POI
from app.config import settings

def enrich_pois(pois_text: list[dict]) -> list[POI]:
    """
    Input: [{"name": "Oslo"}, {"name": "Bergen"}]
    Output: List of POI objects with lat, lon, place_name
    """
    enriched = []

    for poi in pois_text:
        name = poi.get("name")
        if not name:
            continue

        # Mapbox forward geocoding
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{name}.json"
        params = {"access_token": settings.MAPBOX_TOKEN, "limit": 1}
        try:
            resp = requests.get(url, params=params).json()
            features = resp.get("features")
            if features:
                f = features[0]
                enriched.append(
                    POI(
                        name=name,
                        lat=f["center"][1],
                        lon=f["center"][0],
                        place_name=f["place_name"]
                    )
                )
        except Exception as e:
            print(f"Failed to enrich {name}: {e}")

    return enriched

def parse_blog_to_pois(url: str) -> list[dict]:
    """
    Mock function: in MVP, just return some dummy POIs for the given blog URL.
    Later, replace with real LLM logic to extract POIs from the page content.
    """
    return [
        {"name": "Oslo"},
        {"name": "Bergen"},
        {"name": "Trondheim"}
    ]
