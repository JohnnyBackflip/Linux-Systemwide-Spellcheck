import os
import json
from pathlib import Path

DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
DEFAULT_PROMPT = "Correct the spelling and grammar of the following text. Only return the corrected text, no conversational filler or explanation."
DEFAULT_LANG = "en"

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "linux_spellcheck"
        self.config_file = self.config_dir / "config.json"
        
        self.settings = {
            "api_key": "",
            "model": DEFAULT_MODEL,
            "system_prompt": DEFAULT_PROMPT,
            "language": DEFAULT_LANG
        }
        self.load()

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            self.save()

    def save(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
