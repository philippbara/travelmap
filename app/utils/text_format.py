import json
import trafilatura
from json_repair import repair_json


def html_to_clean_text(html: str) -> str:
    result = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        include_links=False,
        include_images=False,
        favor_recall=True,  # capture long-form text
    )
    return result.strip() if result else ""


def markdown_to_json(markdown: str):
    try:
        cleaned = repair_json(markdown)
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {e}")
