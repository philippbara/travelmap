import pytest
from unittest.mock import patch
import json


@pytest.mark.asyncio
async def test_generate_route(client, fake_ai_json_str, mapbox_mock):

    body = json.loads(fake_ai_json_str)

    with (
        patch("app.services.poi_enrichment.requests.get", side_effect=mapbox_mock),
        patch("app.routes.api.save_map", return_value="map-id-123") as mock_save,
    ):
        response = await client.post("/api/generate", json=body)

    assert response.status_code == 200
    data = response.json()

    assert data["map_id"] == "map-id-123"
    assert data["count"] == 5  # all enriched
    mock_save.assert_called_once()


@pytest.mark.asyncio
async def test_llm_parse_route(
    client, example_url, fake_html, fake_ai_json_str, mapbox_mock
):

    with (
        patch("app.services.poi_enrichment.scrape_webpage", return_value=fake_html),
        patch("app.services.poi_enrichment.ai_request", return_value=fake_ai_json_str),
        patch("app.services.poi_enrichment.requests.get", side_effect=mapbox_mock),
        patch("app.routes.api.save_map", return_value="map-999") as mock_save,
    ):
        response = await client.post("/api/llm_parse", json={"url": example_url})

    assert response.status_code == 200
    data = response.json()
    assert data["map_id"] == "map-999"
    assert data["count"] == 5
    mock_save.assert_called_once()
