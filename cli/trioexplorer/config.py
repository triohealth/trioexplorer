"""Configuration management for the Trioexplorer CLI."""

import os
from typing import Optional

from dotenv import load_dotenv, find_dotenv

# Load environment from nearest .env (repo root or cwd)
load_dotenv(find_dotenv(usecwd=True))

# Environment variable names
API_KEY_ENV = "TRIOEXPLORER_API_KEY"
API_URL_ENV = "TRIOEXPLORER_API_URL"

# Default values - production API
DEFAULT_API_URL = "http://k8s-notesear-notesear-160a47ece7-8f008a1f822228b2.elb.us-east-1.amazonaws.com:8001"


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
            f"Set {API_KEY_ENV} in your environment or .env file.\n"
            f"To get an API key, contact sales@trioehealth.com"
        )
    return api_key
