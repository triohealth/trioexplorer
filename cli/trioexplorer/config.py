"""Configuration management for the Trioexplorer CLI."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv, find_dotenv

# System-wide config directory
SYSTEM_CONFIG_DIR = Path.home() / ".trioexplorer"
SYSTEM_ENV_FILE = SYSTEM_CONFIG_DIR / ".env"

# Load environment files in order (later loads don't override existing values):
# 1. System-wide config (~/.trioexplorer/.env) - loaded first, takes priority
# 2. Local .env (repo root or cwd) - fallback for project-specific overrides
load_dotenv(SYSTEM_ENV_FILE)
load_dotenv(find_dotenv(usecwd=True))

# Environment variable names
API_KEY_ENV = "TRIOEXPLORER_API_KEY"
API_URL_ENV = "TRIOEXPLORER_API_URL"

# Default values - production API
DEFAULT_API_URL = "https://search.trioexplorer.com"


def get_api_url(override: Optional[str] = None) -> str:
    """Get the Search API base URL.

    Priority:
    1. Command-line override (--api-url)
    2. Environment variable (TRIOEXPLORER_API_URL)
    3. Default production URL
    """
    if override:
        return override.rstrip("/")

    env_url = os.getenv(API_URL_ENV)
    if env_url:
        return env_url.rstrip("/")

    return DEFAULT_API_URL


def get_api_key() -> Optional[str]:
    """Get the API key from environment.

    Returns None if not set, which will cause auth errors.
    """
    return os.getenv(API_KEY_ENV)


def validate_api_key() -> str:
    """Get and validate the API key.

    Raises:
        SystemExit: If API key is not configured.
    """
    api_key = get_api_key()
    if not api_key:
        raise SystemExit(
            f"Error: No API key configured.\n"
            f"Set {API_KEY_ENV} in one of:\n"
            f"  1. {SYSTEM_ENV_FILE} (recommended for personal use)\n"
            f"  2. .env file in your project directory\n"
            f"  3. Environment variable\n"
            f"To get an API key, contact salessupportdesk@triohealth.com"
        )
    return api_key
