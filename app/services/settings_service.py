"""
AL-HUDA Settings Service — Step 14

Safe, non-destructive settings storage for the AL-HUDA Kivy app.
This module does not replace existing screens or main.py.
"""

import json
from pathlib import Path

DEFAULT_SETTINGS = {
    "language": "English",
    "translation_language": "Urdu + English",
    "theme": "Islamic Dark",
    "notifications": True,
    "azan_notifications": True,
    "azan_sound": True,
    "vibration": True,
    "qibla_compass": True,
    "auto_location": True,
    "font_scale": 1.0,
}

def _settings_path() -> Path:
    """Return a writable per-app settings location when Kivy is running."""
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app is not None:
            path = Path(app.user_data_dir) / "settings.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
    except Exception:
        pass

    path = Path.home() / ".al_huda" / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def load_settings() -> dict:
    settings = DEFAULT_SETTINGS.copy()
    try:
        data = json.loads(_settings_path().read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in DEFAULT_SETTINGS:
                if key in data:
                    settings[key] = data[key]
    except (OSError, ValueError, TypeError):
        pass
    return settings

def save_settings(values: dict) -> dict:
    settings = DEFAULT_SETTINGS.copy()
    if isinstance(values, dict):
        for key in DEFAULT_SETTINGS:
            if key in values:
                settings[key] = values[key]

    path = _settings_path()
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp.replace(path)
    return settings

def set_setting(key: str, value):
    if key not in DEFAULT_SETTINGS:
        raise KeyError(f"Unknown AL-HUDA setting: {key}")
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

def get_setting(key: str):
    if key not in DEFAULT_SETTINGS:
        raise KeyError(f"Unknown AL-HUDA setting: {key}")
    return load_settings()[key]

def reset_settings() -> dict:
    return save_settings(DEFAULT_SETTINGS.copy())
