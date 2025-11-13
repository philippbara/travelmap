import re
import json
from bs4 import BeautifulSoup, Comment

def html_to_text(html: str) -> str:
    """
    A simple HTML cleaner that removes tags and returns plain text.
    """

    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title and body
    title = soup.title.string.strip()
    body = soup.body

    # Remove links etc.
    for tag in body.find_all(['a', 'script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript']):
        tag.decompose()

    # Remove navigation elements
    for nav in body.find_all(class_=['nav', 'navigation', 'menu']):
        nav.decompose()

    # Remove comments
    for comment in body.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove hidden elements
    for el in body.select('[style*="display:none"], [style*="visibility:hidden"]'):
        el.decompose()


    text = body.get_text(separator='\n', strip=True)

    # Collapse multiple newlines, minimize tokens
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Collapse multiple spaces/tabs
    text = re.sub(r'[ \t]+', ' ', text)    

    text = f"Title: {title}\n{text}"

    return text

def markdown_to_json(markdown: str) -> str:
    # Strip markdown code blocks
    markdown = markdown.strip()
    
    # Remove leading text before JSON
    if "```json" in markdown:
        markdown = markdown.split("```json")[1].split("```")[0].strip()
    elif "```" in markdown:
        markdown = markdown.split("```")[1].split("```")[0].strip()
    
    # Remove any leading explanatory text (look for first '[')
    if not markdown.startswith('['):
        json_start = markdown.find('[')
        if json_start != -1:
            markdown = markdown[json_start:]
    
    # Remove any trailing text after JSON (look for last ']')
    if not markdown.endswith(']'):
        json_end = markdown.rfind(']')
        if json_end != -1:
            markdown = markdown[:json_end + 1]

    return json.loads(markdown)