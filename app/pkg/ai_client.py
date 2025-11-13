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

SYSTEM_MESSAGE = SYSTEM_MESSAGE = """
You are a data extraction assistant specialized in travel content analysis.

The input is a travel blog or trip diary where a traveler describes their journey, destinations, and the places they visited or passed through. 
Your task is to extract only the specific geographic locations that are part of the traveler’s trip or described as visited, explored, or experienced — 
not places mentioned incidentally (e.g., where other people are from or just used for comparison).

A “location” is any physical place that can be mapped — such as a city, town, village, island, beach, mountain, park, hill, viewpoint, lake, river, market, museum, temple, square, or other recognizable destination.

### Extraction rules

1. Identify all distinct, named locations that the traveler visits, passes through, or describes in the travel narrative.

2. Normalize each location to its **most specific, fully qualified, map-identifiable form**, suitable for Mapbox or Google Maps lookup.
   - Always include the **city, region/island, and country** if known or inferable.
   - If the article clearly focuses on one region or country, assume that as the default context for sub-locations (e.g., “Shirley Heights, English Harbour, Antigua and Barbuda”).
   - Examples:
       - “St. John’s, Antigua and Barbuda” — city
       - “Bondi Beach, Sydney, Australia” — beach
       - “Mount Fuji, Honshu, Japan” — mountain
       - “Central Park, New York City, USA” — park
       - “Shirley Heights, English Harbour, Antigua and Barbuda” — viewpoint
       - “Tsukiji Outer Market, Tokyo, Japan” — market
       - “The Roxy, New York City, USA” — venue
       - “Santorini, Greece” — island
       - “Lake Bled, Slovenia” — lake
       - “Wat Arun Temple, Bangkok, Thailand” — temple
       - “The beach of Nice, France” — beach (city-linked)

3. If a place name is ambiguous, infer the correct one using context such as nearby places, country, or described route.

4. Exclude:
   - Mentions of where locals or others are from.
   - Generic references like “the coast,” “the city,” or “the hotel.”
   - Places that are not part of the traveler’s actual route or experience.

### Output format

Return a JSON array with **only one property per entry**:

[
  { "name": "St. John's, Antigua and Barbuda" },
  { "name": "Bondi Beach, Sydney, Australia" },
  { "name": "Mount Fuji, Honshu, Japan" },
  { "name": "Central Park, New York City, USA" },
  { "name": "Shirley Heights, English Harbour, Antigua and Barbuda" },
  { "name": "Lake Bled, Slovenia" },
  { "name": "Wat Arun Temple, Bangkok, Thailand" }
]

Each “name” must be:
- Fully qualified (city/region/country when available).
- Unique, precise, and geocoding-ready.
- Relevant to the traveler’s own trip or described route.
"""


USER_MESSAGE = """
From the following cleaned webpage text, extract all specific geographic locations and output them as a JSON array per the system format.

Text:
{}
"""

