import json
import uuid
from pathlib import Path

MAP_DIR = Path("maps")


def save_map(map_json: dict) -> str:
    """
    Save the entire FeatureCollection JSON returned by the LLM/enrichment step.
    Returns the generated map_id.
    """
    MAP_DIR.mkdir(exist_ok=True)
    map_id = str(uuid.uuid4())
    path = MAP_DIR / f"{map_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(map_json, f, indent=2, ensure_ascii=False)
    return map_id


def load_map(map_id: str) -> dict:
    """
    Load the saved map JSON by map_id.
    """
    path = MAP_DIR / f"{map_id}.json"
    with open(path, encoding="utf-8") as f:
        map_json = json.load(f)
    return map_json
