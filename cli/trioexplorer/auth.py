"""Authentication handling for the Trioexplorer CLI."""

from typing import Optional

from .config import get_api_key, validate_api_key, API_KEY_ENV


def get_auth_headers(require_auth: bool = True) -> dict[str, str]:
    """Get HTTP headers with authentication.

    Args:
        require_auth: If True, raises SystemExit when API key is missing.
                     If False, returns empty headers when API key is missing.

    Returns:
        Dictionary of headers including X-API-Key if available.

    Raises:
        SystemExit: If require_auth is True and API key is not set.
    """
    headers = {}

    if require_auth:
        api_key = validate_api_key()
        headers["X-API-Key"] = api_key
    else:
        api_key = get_api_key()
        if api_key:
            headers["X-API-Key"] = api_key

    return headers


def check_auth_error(status_code: int, response_text: str) -> Optional[str]:
    """Check if an HTTP error is authentication-related.

    Args:
        status_code: HTTP status code
        response_text: Response body text

    Returns:
        User-friendly error message if auth error, None otherwise.
    """
    if status_code == 401:
        return (
            f"Authentication failed - Invalid or expired API key.\n"
            f"Please check your {API_KEY_ENV} environment variable."
        )
    elif status_code == 403:
        return (
            f"Authorization denied - Your API key does not have permission for this operation.\n"
            f"Contact your administrator to request access."
        )
    return None
