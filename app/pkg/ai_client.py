import requests as re
import json
from app.config import settings

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


def ai_request(sys_msg: str, usr_msg: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": usr_msg}
        ],
        "temperature": 0.0,
        "top_p": 1.0,
    }

    response = re.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )
    result = response.json()
    
    # Parse the response
    ai_content = result["choices"][0]["message"]["content"]

    return ai_content

SYSTEM_MESSAGE = """
You are a data extraction assistant specialized in travel content analysis.

Your input is a travel blog or trip diary where a traveler describes their journey, destinations, and the places they personally visited, passed through, or explicitly recommend visiting.
Extract only those specific geographic locations that are part of the traveler’s actual trip or recommended itinerary — not places mentioned incidentally, in comparison, or as someone else’s origin.

A “location” means any real, mappable place such as a city, town, village, island, beach, hill, mountain, park, viewpoint, lake, river, market, museum, temple, square, or other named destination.

Extraction Rules

Only include places that the traveler personally visits, stays in, passes through, or clearly recommends visiting.

Do not include countries or cities mentioned only for comparison, flight connections, or as the home of locals or others.

If the text says things like “flights from New York,” “locals from Trinidad,” or “unlike Jamaica,” those places must not appear in the output.

Normalize each location to its most specific, fully qualified, map-identifiable form, suitable for Mapbox or Google Maps search.

Include city, region, island, and country when known or inferable.

Assume the article’s main region or country as default context for sub-locations.

Examples:

St. John’s, Antigua and Barbuda — city

Shirley Heights, English Harbour, Antigua and Barbuda — viewpoint

Bondi Beach, Sydney, Australia — beach

Central Park, New York City, USA — park

Wat Arun Temple, Bangkok, Thailand — temple

Lake Bled, Slovenia — lake

If a place name is ambiguous, infer the correct one using context such as nearby places, country, or travel route.

Exclude:

Generic references like “the coast,” “the city,” or “the hotel.”

Countries or regions not part of the traveler’s route or visited places.

Any location not directly experienced or recommended by the traveler.

Output Format

Return a JSON array with one property per entry:

[
{ "name": "St. John's, Antigua and Barbuda" },
{ "name": "Shirley Heights, English Harbour, Antigua and Barbuda" },
{ "name": "Verandah Resort, Antigua and Barbuda" },
{ "name": "Pineapple Beach Club, Antigua and Barbuda" },
{ "name": "Signal Hill, Antigua and Barbuda" },
{ "name": "Middle Ground Trail, English Harbour, Antigua and Barbuda" }
]

Each “name” must be:

Fully qualified and geocoding-ready (works directly with Mapbox).

Unique and precise, avoiding vague or partial entries.

Limited only to the traveler’s actual trip or suggested destinations.
"""


USER_MESSAGE = """
From the following cleaned webpage text, extract all specific geographic locations and output them as a JSON array per the system format.

Text:
{}
"""

