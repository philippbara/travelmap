import requests
from app.config import settings
from app.pkg.ai_client import ai_request_async, SYSTEM_MESSAGE, USER_MESSAGE
from app.pkg.scrape import scrape_webpage
from app.utils.text_format import html_to_clean_text, markdown_to_json

from app.logger import setup_logger

logger = setup_logger(__name__)


def enrich_pois(features: list[dict]) -> list[dict]:
    """
    Input: features from LLM JSON:
    [
        {
            "type": "Feature",
            "properties": {
                "name": "Oslo",
                "category": "city",
                "country_code": "NO",
                "order": 1,
                "description": "...",
                "link": "..."
            }
        },
        ...
    ]
    Output: same features with "geometry" added (lat/lon) using Search Box API
    """

    logger.info("Enriching %d POIs using Mapbox Search Box API", len(features))
    enriched = []

    for feature in features:
        props = feature.get("properties", {})
        name = props.get("name")
        country = props.get("country_code")
        category = props.get("category")
        if not name or not country:
            continue

        # Mapbox Search Box Forward API
        url = "https://api.mapbox.com/search/searchbox/v1/forward"
        params = {
            "q": name,
            "access_token": settings.MAPBOX_TOKEN,
            "limit": 1,
            "language": "en",
            "country": country.upper(),
        }

        # Optionally include poi_category if provided
        if category:
            params["poi_category"] = category

        try:
            resp = requests.get(url, params=params, timeout=10).json()
            results = resp.get("features")
            if results:
                f = results[0]

                # Extract coordinates from geometry if available
                coords = f.get("geometry", {}).get("coordinates")
                if coords and len(coords) == 2:
                    feature["geometry"] = {
                        "type": "Point",
                        "coordinates": coords
                    }
                    enriched.append(feature)
                else:
                    logger.warning("No geometry coordinates for POI: %s (%s)", name, country)
            else:
                logger.warning("No search result for POI: %s (%s)", name, country)
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

    ai_response = await ai_request_async(SYSTEM_MESSAGE, USER_MESSAGE.format(blog_text))

    logger.info("Received AI response, length: %d", len(ai_response))

    pois_dict = markdown_to_json(ai_response)

    pois_names = [poi.get("name") for poi in pois_dict if poi.get("name")]
    logger.info("Parsed POIs from AI response: %s", pois_names)
    logger.info("Total POIs extracted: %d", len(pois_dict))

    return pois_dict
