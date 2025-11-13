import re
import json
from bs4 import BeautifulSoup, Comment

def html_to_text(html: str) -> str:
    """
    Converts HTML to clean plain text optimized for travel content extraction.
    Removes boilerplate (navs, footers, affiliate disclaimers, subscribe prompts, etc.),
    strips booking blurbs and fragments, and normalizes whitespace.
    Works reliably on 80–90% of travel blogs.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Extract title (safe fallback)
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    body = soup.body or soup

    # Remove non-content tags
    for tag in body.find_all([
        "a", "script", "style", "nav", "header", "footer", "aside",
        "iframe", "noscript", "form", "svg", "figure"
    ]):
        tag.decompose()

    # Remove elements with common non-content classes/ids
    for el in body.find_all(attrs={"class": True, "id": True}):
        class_id = " ".join(el.get("class", [])) + " " + el.get("id", "")
        if any(k in class_id.lower() for k in [
            "nav", "menu", "comment", "share", "footer", "header",
            "subscribe", "newsletter", "related", "promo", "advert"
        ]):
            el.decompose()

    # Remove comments
    for comment in body.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove hidden elements
    for el in body.select("[style*='display:none'], [style*='visibility:hidden']"):
        el.decompose()

    # Extract plain text
    text = body.get_text(separator="\n", strip=True)

    # Remove boilerplate lines by common keywords (site-agnostic)
    boilerplate = re.compile(
        r"(?i)\b("
        r"affiliate|sponsored|subscribe|unsubscribe|privacy|cookies|"
        r"comment|follow|tweet|pinterest|share|promo|offer|deal|discount|"
        r"advert|terms|policy|login|signup|copyright|©"
        r")\b"
    )
    lines = [line for line in text.splitlines()
             if len(line.strip()) > 2 and not boilerplate.search(line)]

    text = "\n".join(lines)

    # --- Extra cleanup steps (generic, high-impact) ---
    # 1. Remove "Essential Info" and booking blurbs
    text = re.sub(r"(?is)essential info:.*", "", text)
    text = re.sub(r"(?i)\b(book(ing)?|rates?|prices?|insurance|emailing|hosted by)\b.*", "", text)

    # 2. Drop orphan / fragment lines (too short to be narrative)
    text = "\n".join(line for line in text.splitlines() if len(line.split()) > 2)

    # 3. Normalize whitespace and punctuation
    text = re.sub(r"\s+", " ", text).strip()

    # Optional 4️⃣: keep only travel-related paragraphs (geo cues)
    # geo_cues = (" in ", " at ", " to ", " from ", " near ", " through ", " around ",
    #             "visited", "stayed", "drove", "hiked", "flew", "explored")
    # text = "\n".join(p for p in text.split(". ") if any(cue in p.lower() for cue in geo_cues))

    if title:
        text = f"Title: {title}\n{text}"

    return text.strip()

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
            markdown = markdown[:json_end + 1]

    return json.loads(markdown)