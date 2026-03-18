import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

class Config:
    """Centralized configuration management."""
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
    SHEET_RANGE: str = os.getenv("SHEET_RANGE", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    @classmethod
    def validate_google_config(cls) -> list[str]:
        errors = []
        if not cls.GOOGLE_APPLICATION_CREDENTIALS or not os.path.exists(cls.GOOGLE_APPLICATION_CREDENTIALS):
            errors.append("GOOGLE_APPLICATION_CREDENTIALS file is missing or invalid.")
        if not cls.SPREADSHEET_ID:
            errors.append("SPREADSHEET_ID is missing.")
        if not cls.SHEET_RANGE:
            errors.append("SHEET_RANGE is missing.")
        return errors
