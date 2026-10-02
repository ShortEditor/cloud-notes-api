"""Configuration read from environment variables (twelve-factor style)."""
import os


def load():
    return {
        "port": int(os.environ.get("PORT", "8080")),
        "log_level": os.environ.get("LOG_LEVEL", "INFO").upper(),
        "max_notes": int(os.environ.get("MAX_NOTES", "100")),
    }
