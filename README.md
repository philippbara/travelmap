Travel Map Generator
====================

A small FastAPI project that allows users to generate interactive maps from travel blog POIs or custom JSON. Built with FastAPI, Mapbox, and Jinja2 templates.

**Features**
------------

*   Extract POIs from travel blog text using LLM

*   Fetches content from blogs using Playwright (headless browser)

*   Upload JSON containing POIs (name only).
    
*   Automatically enriches POIs with coordinates using Mapbox Geocoding API.
    
*   Generates an interactive map with markers for each POI.
    
*   Frontend dashboard to view maps.
    
*   API endpoint for programmatic map generation.
    

**Setup**
---------

1.  Clone the repository:
    

`   git clone   cd travel-map-generator   `

2.  Create a virtual environment and install dependencies:
    
`   python -m venv venv  source venv/bin/activate   # On Windows: venv\Scripts\activate  pip install -r requirements.txt   `

3. Install playwright

` playwright install `

4.  Create a .env file with your Mapbox token:

```
MAPBOX_TOKEN=your_mapbox_token_here
OPENROUTER_API_KEY=your_openrouter_token_here
```
5.  Run the app:
    
`   uvicorn app.main:app --reload   `

6.  Open [http://localhost:8000](http://localhost:8000) in your browser.
    

**Usage**
---------

1.  On the homepage, paste or upload JSON like:
    
`   [    {"name": "Oslo"},    {"name": "Bergen"}  ]   `

    Or insert the URL and it will parse the data automatically.

2.  Click **Generate Map**.
    
3.  You will be redirected to /map/{map\_id} to view the interactive map.
    

**API**
-------

*   **POST** /api/generateAccepts JSON array of POIs (text-only) and returns:
    
`   {    "map_id": "uuid",    "count": 3  }   `

*   **Frontend routes**:
    
    *   / → homepage with upload form
        
    *   /map/{map\_id} → display map
        

**Notes**
---------

*   Generated maps are saved in maps/.
    
*   \_\_pycache\_\_/, maps/, and .env are ignored in Git.
    
*   Mapbox Geocoding is used to enrich POIs; only the first result is taken.