from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Flat Swap API"
    API_V1_STR: str = "/api/v1"
    
    
    
    # Auth0 Settings
    AUTH0_DOMAIN: str = "dev-ys7wykggrb6ms4qq.us.auth0.com"
    AUTH0_API_AUDIENCE: str = "http://localhost:8000"
    AUTH0_ALGORITHMS: List[str] = ["RS256"]
    
    DATABASE_URL: str = "sqlite:///./flat_swap.db"
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If it's not valid JSON, try splitting by comma
                return [origin.strip() for origin in v.split(',')]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()

