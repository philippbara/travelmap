import requests
from app.models.poi import POI
from app.config import settings
from app.pkg.ai_client import ai_request_async, SYSTEM_MESSAGE, USER_MESSAGE
from app.pkg.scrape import scrape_webpage
from app.utils.text_format import html_to_clean_text, markdown_to_json

from app.logger import setup_logger

logger = setup_logger(__name__)


def enrich_pois(pois_text: list[dict]) -> list[POI]:
    """
    Input: [{"name": "Oslo"}, {"name": "Bergen"}]
    Output: list of POI objects with lat, lon, place_name
    """

    logger.info("Enriching %d POIs using Mapbox Geocoding API", len(pois_text))

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
                        place_name=f["place_name"],
                    )
                )
            else:
                logger.warning("No geocoding result for POI: %s", name)
        except Exception as e:
            logger.error("Failed to enrich POI '%s': %s", name, e)

    logger.info("Enriched %d POIs", len(enriched))

    return enriched


async def parse_blog_to_pois(url: str) -> list[dict]:
    logger.info("Scraping blog URL: %s", url)

    blog_content = await scrape_webpage(url)

    logger.info("Scraped blog content length: %d", len(blog_content))

    blog_text = html_to_clean_text(blog_content)

    logger.info("Converted blog content to text, length: %d", len(blog_text))

    logger.info("Sending text to AI for POI extraction")

    ai_response = await ai_request_async(
        {
            "OPENROUTER_API_KEY": settings.OPENROUTER_API_KEY,
            "OPENROUTER_URL": "https://openrouter.ai/api/v1/chat/completions",
            "OPENROUTER_MODEL": "meta-llama/llama-3.3-70b-instruct:free",
        },
        SYSTEM_MESSAGE,
        USER_MESSAGE.format(blog_text),
    )

    logger.info("Received AI response, length: %d", len(ai_response))

    pois_json = markdown_to_json(ai_response)

    # Add in to mask the dict. Improve in the future. TO CHANGE
    pois_json = [
        {"name": feature["properties"].get("name", "")}
        for feature in pois_json["features"]
    ]

    logger.info("Parsed POIs from AI response: %s", pois_json)
    logger.info("Total POIs extracted: %d", len(pois_json))

    return pois_json
