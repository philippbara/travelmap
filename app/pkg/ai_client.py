import httpx
from app.config import settings

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


async def ai_request_async(sys_msg: str, usr_msg: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": usr_msg},
        ],
        "temperature": 0.0,
        "top_p": 1.0,
    }

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
        )

    result = response.json()

    # Parse OpenRouter response safely
    try:
        ai_content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Invalid response from AI API: {result}") from e

    return ai_content


SYSTEM_MESSAGE = """
You extract travel-relevant POIs from a travel article. Your first task is to detect the primary trip being described. Extract only POIs inside this trip region. Ignore all references to any other country, region, island, city, comparison, origin, flight hub, anecdote, or unrelated travel.

TRIP SCOPE RULE (MANDATORY)
Determine the main destination region/country of the trip.
Extract only POIs located inside this region.
Exclude all other places (comparisons, origins, flight origins, unrelated destinations, generic references).

INCLUSION RULE
Include only places the traveler visited, stayed, passed through, or explicitly recommends as part of this trip.
FULL QUALIFICATION RULE (MANDATORY)
Every POI must be output as a fully qualified, geocoding-ready name:

<poi>, <local area / neighbourhood>, <city / town>, <region / island>, <country>


Rules:
Always include the country.
Include intermediate hierarchy levels when available or inferable.
If hierarchy is unknown, use <poi>, <country>.
Never output an unqualified POI.
All names must be real and geocodable.

CATEGORY RULE (STRICT)
category must be exactly one valid Mapbox Searchbox category from:
https://api.mapbox.com/search/searchbox/v1/list/category
No made-up categories. No synonyms. No approximations.

NORMALIZATION RULE
Deduplicate POIs.
Assign correct ISO-3166 alpha-2 country code.
Determine strict narrative order of POIs.
Use the article’s geographic context to infer missing details.

OUTPUT FORMAT
Return only:

{
  "type": "FeatureCollection",
  "properties": {
    "title": "<short itinerary title>",
    "description": "<1-sentence summary>"
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "order": <int>,
        "name": "<fully qualified POI name>",
        "category": "<valid_mapbox_category>",
        "country_code": "<ISO-3166 alpha-2>",
        "description": "<multi-sentence description>",
        "link": "<optional>"
      }
    }
  ]
}

STRICT VALIDATION
JSON only.
All POIs must be within the main trip region.
All names must be fully qualified.
All categories must be valid Mapbox categories.
No commentary.
"""


USER_MESSAGE = """
From the following cleaned webpage text, extract all specific geographic locations and output them as a JSON array per the system format.

Text:
{}
"""
