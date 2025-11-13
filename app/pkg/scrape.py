from playwright.sync_api import sync_playwright

def scrape_webpage(url: str) -> str:
    with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            
            context = browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
            )
            
            page = context.new_page()
            
            # Hide webdriver detection
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            page.goto(url, wait_until='networkidle')
            content = page.content()
            
            browser.close()
            
            return content