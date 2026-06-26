import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "scholar sync"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL")
    GEMINI_TEMPERATURE: str = os.getenv("GEMINI_TEMPERATURE")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    LOG_LEVEL: str = "DEBUG"
    MAX_PDF_PAGES: int = int(os.getenv('MAX_PDF_PAGES'))

    class Config:
        case_sensitive = True
        extra = "ignore"

settings = Settings()