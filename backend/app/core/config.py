import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "scholar sync"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    LOG_LEVEL: str = "DEBUG"

    class Config:
        case_sensitive = True
        extra = "ignore"

settings = Settings()