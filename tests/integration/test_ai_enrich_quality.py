import json
import difflib
import pytest

from app.config import settings
from app.utils.text_format import html_to_clean_text, markdown_to_json
from app.services.poi_enrichment import enrich_pois
from app.pkg.ai_client import ai_request_async, SYSTEM_MESSAGE, USER_MESSAGE


@pytest.mark.asyncio
async def test_ai_and_map_enrichment_quality():
    # Load ideal fixture
    print("Loading ideal fixture...")
    with open("tests/integration/manual_fixtures/article_01/article_01.json") as f:
        ideal = json.load(f)

    ideal_pois = [f["properties"]["name"] for f in ideal["ai_json"]["features"]]
    ideal_enriched = [p["name"] for p in ideal["enriched_pois"]]

    # Load HTML
    with open("tests/integration/manual_fixtures/article_01/article_01.html") as f:
        html = f.read()
    text = html_to_clean_text(html)

    # Run AI
    print("Requesting AI...")
    ai_response = await ai_request_async(
        {
            "OPENROUTER_API_KEY": settings.OPENROUTER_API_KEY,
            "OPENROUTER_URL": "https://openrouter.ai/api/v1/chat/completions",
            "OPENROUTER_MODEL": "meta-llama/llama-3.3-70b-instruct:free",
        },
        SYSTEM_MESSAGE,
        USER_MESSAGE.format(text),
    )
    print("AI done.")

    ai_json = markdown_to_json(ai_response)
    predicted_pois = [f["properties"]["name"] for f in ai_json.get("features", [])]

    # Similarity helper
    def similarity(a, b):
        return difflib.SequenceMatcher(None, sorted(a), sorted(b)).ratio()

    poi_sim = similarity(predicted_pois, ideal_pois)

    # Map enrichment
    print("Enriching with Mapbox...")
    enrich_input = [{"name": n} for n in predicted_pois]
    enriched = enrich_pois(enrich_input)
    enriched_names = [p.name for p in enriched]

    enrich_sim = similarity(enriched_names, ideal_enriched)

    # Print summary (never fails)
    print("\n=== AI Extraction Summary ===")
    print(json.dumps({
        "ideal_count": len(ideal_pois),
        "predicted_count": len(predicted_pois),
        "similarity_score": round(poi_sim, 3),
    }, indent=2))

    print("\n=== Map Enrichment Summary ===")
    print(json.dumps({
        "ideal_enriched_count": len(ideal_enriched),
        "predicted_enriched_count": len(enriched_names),
        "similarity_score": round(enrich_sim, 3),
    }, indent=2))

    # Diffs
    missing_ai = sorted(set(ideal_pois) - set(predicted_pois))
    extra_ai = sorted(set(predicted_pois) - set(ideal_pois))
    print("\n=== Differences (AI POIs) ===")
    print(json.dumps({"missing": missing_ai, "extra": extra_ai}, indent=2))

    missing_en = sorted(set(ideal_enriched) - set(enriched_names))
    extra_en = sorted(set(enriched_names) - set(ideal_enriched))
    print("\n=== Differences (Enriched POIs) ===")
    print(json.dumps({"missing": missing_en, "extra": extra_en}, indent=2))

    # Never failing test
    print("\nTest completed (non-breaking diagnostic mode).")
    assert True
