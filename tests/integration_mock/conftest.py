import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


# -------------------------------------------------------
# HTTP client fixture
# -------------------------------------------------------
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# -------------------------------------------------------
# Example URL used by llm_parse tests
# -------------------------------------------------------
@pytest.fixture
def example_url():
    return "https://www.theguardian.com/travel/2025/nov/13/chatsworth-house-derbyshire-new-family-friendly-hotel"


# -------------------------------------------------------
# Fake AI FeatureCollection (LLM output)
# -------------------------------------------------------
@pytest.fixture
def fake_ai_json():
    return {
        "type": "FeatureCollection",
        "properties": {
            "title": "Slovenia Highlights",
            "description": "Extracted itinerary based on a sample travel article.",
        },
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "order": 1,
                    "name": "Lake Bled, Slovenia",
                    "category": "lake",
                    "country_code": "SI",
                    "description": "A glacial lake in the Julian Alps, known for its island and medieval castle.",
                    "link": None,
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "order": 2,
                    "name": "Ljubljana, Slovenia",
                    "category": "city",
                    "country_code": "SI",
                    "description": "Slovenia’s capital city with vibrant cultural and historical sites.",
                    "link": None,
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "order": 3,
                    "name": "Bled Island, Lake Bled, Slovenia",
                    "category": "island",
                    "country_code": "SI",
                    "description": "A small island on Lake Bled featuring a prominent church.",
                    "link": None,
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "order": 4,
                    "name": "Bled Castle, Bled, Slovenia",
                    "category": "castle",
                    "country_code": "SI",
                    "description": "A medieval castle perched above Lake Bled with panoramic views.",
                    "link": None,
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "order": 5,
                    "name": "Ojstrica Viewpoint, Bled, Slovenia",
                    "category": "viewpoint",
                    "country_code": "SI",
                    "description": "A hilltop viewpoint offering iconic panoramic views of Lake Bled.",
                    "link": None,
                },
            },
        ],
    }


# -------------------------------------------------------
# /api/generate input (list[dict] with {"name": ...})
# -------------------------------------------------------
@pytest.fixture
def fake_generate_input(fake_ai_json):
    import json
    return json.dumps([
        {"name": feature["properties"]["name"]}
        for feature in fake_ai_json["features"]
    ])


# -------------------------------------------------------
# /api/llm_parse: LLM raw output (FULL FeatureCollection)
# -------------------------------------------------------
@pytest.fixture
def fake_llm_response(fake_ai_json):
    import json
    return json.dumps(fake_ai_json)


# -------------------------------------------------------
# Mapbox mock (matching fully qualified names)
# -------------------------------------------------------
@pytest.fixture
def fake_mapbox_json():
    return {
        "Lake Bled, Slovenia": [14.0937, 46.3625],
        "Ljubljana, Slovenia": [14.5058, 46.0569],
        "Bled Island, Lake Bled, Slovenia": [14.0949, 46.3637],
        "Bled Castle, Bled, Slovenia": [14.1010, 46.3692],
        "Ojstrica Viewpoint, Bled, Slovenia": [14.0875, 46.3594],
    }


@pytest.fixture
def mapbox_mock(fake_mapbox_json):
    from types import SimpleNamespace

    def _side_effect(url, params):
        name = url.split("/")[-1].replace(".json", "")
        coords = fake_mapbox_json.get(name)

        if coords:
            return SimpleNamespace(
                json=lambda: {
                    "features": [
                        {
                            "center": coords,
                            "place_name": name,
                        }
                    ]
                }
            )

        return SimpleNamespace(json=lambda: {"features": []})

    return _side_effect


# -------------------------------------------------------
# Blog HTML content for scraping
# -------------------------------------------------------
@pytest.fixture
def fake_html():
    return """
    <html>
    <body>
        <p>We visited Lake Bled and Ljubljana.</p>
        <p>Then explored Bled Island and Bled Castle.</p>
        <p>Finished at Ojstrica Viewpoint.</p>
    </body>
    </html>
    """
