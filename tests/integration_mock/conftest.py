import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def example_url():
    return "https://www.theguardian.com/travel/2025/nov/13/chatsworth-house-derbyshire-new-family-friendly-hotel"


@pytest.fixture
def fake_ai_json():
    return [
        {"name": "Lake Bled"},
        {"name": "Ljubljana"},
        {"name": "Bled Island"},
        {"name": "Bled Castle"},
        {"name": "Ojstrica Viewpoint"},
    ]


@pytest.fixture
def fake_ai_json_str(fake_ai_json):
    import json
    return json.dumps(fake_ai_json)


@pytest.fixture
def fake_mapbox_json():
    return {
        "Lake Bled":  [14.0937, 46.3625],
        "Ljubljana":  [14.5058, 46.0569],
        "Bled Island": [14.0949, 46.3637],
        "Bled Castle": [14.1010, 46.3692],
        "Ojstrica Viewpoint": [14.0875, 46.3594],
    }


@pytest.fixture
def mapbox_mock(fake_mapbox_json):
    """Generate a correct Mapbox mock response."""
    from types import SimpleNamespace

    def _side_effect(url, params):
        name = url.split("/")[-1].replace(".json", "")
        coords = fake_mapbox_json.get(name)
        if coords:
            return SimpleNamespace(json=lambda: {
                "features": [{
                    "center": coords,
                    "place_name": name,    # REQUIRED by your code
                }]
            })
        return SimpleNamespace(json=lambda: {"features": []})

    return _side_effect


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
