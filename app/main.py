from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import dashboard, api

app = FastAPI(title="Travel Map Generator")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(dashboard.router)
app.include_router(api.router)
