import requests
from app.models.poi import POI
from app.config import settings
from app.pkg.ai_client import ai_request, SYSTEM_MESSAGE, USER_MESSAGE
from app.pkg.scrape import scrape_webpage
from app.utils.text_format import html_to_text, markdown_to_json

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


def parse_blog_to_pois(url: str) -> list[dict]:
    logger.info("Scraping blog URL: %s", url)

    blog_content = scrape_webpage(url)

    logger.info("Scraped blog content length: %d", len(blog_content))

    blog_text = html_to_text(blog_content)

    logger.info("Converted blog content to text, length: %d", len(blog_text))

    logger.info("Sending text to AI for POI extraction")

    ai_response = ai_request(SYSTEM_MESSAGE, USER_MESSAGE.format(blog_text))

    logger.info("Received AI response, length: %d", len(ai_response))

    pois_dict = markdown_to_json(ai_response)

    pois_names = [poi.get("name") for poi in pois_dict if poi.get("name")]
    logger.info("Parsed POIs from AI response: %s", pois_names)
    logger.info("Total POIs extracted: %d", len(pois_dict))

    return pois_dict
