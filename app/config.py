from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAPBOX_TOKEN: str
    OPENROUTER_API_KEY: str
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()