import json
import uuid
from pathlib import Path
from app.models.poi import POI

MAP_DIR = Path("maps")


def save_map(pois: list[POI]) -> str:
    MAP_DIR.mkdir(exist_ok=True)
    map_id = str(uuid.uuid4())
    path = MAP_DIR / f"{map_id}.json"
    with open(path, "w") as f:
        json.dump([poi.dict() for poi in pois], f, indent=2)
    return map_id


def load_map(map_id: str) -> list[POI]:
    path = MAP_DIR / f"{map_id}.json"
    with open(path) as f:
        pois_data = json.load(f)
    return [POI(**poi) for poi in pois_data]
