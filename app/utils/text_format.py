import json
import trafilatura


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


def markdown_to_json(markdown: str) -> str:
    # Strip markdown code blocks
    markdown = markdown.strip()

    # Remove leading text before JSON
    if "```json" in markdown:
        markdown = markdown.split("```json")[1].split("```")[0].strip()
    elif "```" in markdown:
        markdown = markdown.split("```")[1].split("```")[0].strip()

    # Remove any leading explanatory text (look for first "[")
    if not markdown.startswith("["):
        json_start = markdown.find("[")
        if json_start != -1:
            markdown = markdown[json_start:]

    # Remove any trailing text after JSON (look for last "]")
    if not markdown.endswith("]"):
        json_end = markdown.rfind("]")
        if json_end != -1:
            markdown = markdown[: json_end + 1]

    return json.loads(markdown)
