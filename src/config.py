import os
import sys
from pathlib import Path

def get_data_dir() -> Path:
    """Returns directory for reading read-only bundled assets (PyInstaller friendly)."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "data"
    return Path(__file__).resolve().parent.parent / "data"

def get_user_data_dir() -> Path:
    """Returns official Windows Local AppData directory for persistent writable storage."""
    local_appdata = os.getenv("LOCALAPPDATA")
    if local_appdata:
        base = Path(local_appdata) / "UIUStudentAssistant"
    else:
        # Fallback for non-Windows environments
        base = Path.home() / ".uiu_student_assistant"

    base.mkdir(parents=True, exist_ok=True)
    return base
