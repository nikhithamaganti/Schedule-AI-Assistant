import os
from pathlib import Path

def ensure_data_dir_exists() -> Path:
    """
    Ensures that the data/ directory exists in the project root.
    Returns the path to the data directory.
    """
    # utils.py is in src/schedule_assistant
    # __file__ -> utils.py
    # parent -> schedule_assistant
    # parent.parent -> src
    # parent.parent.parent -> schedule-assistant-ai (project root)
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data"
    
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        
    return data_dir

def format_error_message(context: str, errors: list[str]) -> str:
    """
    Formats a list of validation errors into a friendly message.
    """
    if not errors:
        return ""
    
    msg = f"### ⚠️ {context} Issues Detected\n"
    for err in errors:
        msg += f"- **{err}**\n"
    msg += "\n*Please correct your `.env` configuration file immediately to proceed.*"
    return msg
