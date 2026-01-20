"""HTTP client for the Search API."""

import sys
from typing import Any, Optional

import httpx
from rich.console import Console

from .config import get_api_url
from .auth import get_auth_headers, check_auth_error

console = Console(stderr=True)

# Default timeout in seconds
DEFAULT_TIMEOUT = 60.0


class SearchClient:
    """HTTP client wrapper for the Search API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        debug: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Initialize the client.

        Args:
            base_url: Override for the API base URL.
            debug: Enable debug logging of requests/responses.
            timeout: Request timeout in seconds.
        """
        self.base_url = get_api_url(base_url)
        self.debug = debug
        self.timeout = timeout
        self.headers = get_auth_headers(require_auth=True)

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details if debug is enabled."""
        if not self.debug:
            return
        console.print(f"[dim]>>> {method} {url}[/dim]")
        if kwargs.get("params"):
            console.print(f"[dim]    params: {kwargs['params']}[/dim]")
        if kwargs.get("json"):
            console.print(f"[dim]    json: {kwargs['json']}[/dim]")

    def _log_response(self, response: httpx.Response) -> None:
        """Log response details if debug is enabled."""
        if not self.debug:
            return
        console.print(f"[dim]<<< {response.status_code} ({len(response.content)} bytes)[/dim]")

    def _handle_error(self, error: Exception, url: str) -> None:
        """Handle request errors with user-friendly messages."""
        if isinstance(error, httpx.HTTPStatusError):
            auth_error = check_auth_error(
                error.response.status_code,
                error.response.text
            )
            if auth_error:
                console.print(f"[red]{auth_error}[/red]")
            else:
                try:
                    detail = error.response.json().get("detail", error.response.text)
                except Exception:
                    detail = error.response.text
                console.print(f"[red]Error {error.response.status_code}: {detail}[/red]")
            sys.exit(1)

        elif isinstance(error, httpx.ConnectError):
            console.print(f"[red]Cannot connect to Search API at {self.base_url}[/red]")
            console.print("[dim]Is the server running?[/dim]")
            sys.exit(1)

        elif isinstance(error, httpx.TimeoutException):
            console.print(f"[red]Request timed out after {self.timeout}s[/red]")
            sys.exit(1)

        elif isinstance(error, httpx.RequestError):
            console.print(f"[red]Network error: {error}[/red]")
            sys.exit(1)

        else:
            console.print(f"[red]Unexpected error: {error}[/red]")
            sys.exit(1)

    def get(self, path: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a GET request to the API.

        Args:
            path: API endpoint path (e.g., "/search")
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            SystemExit: On any request error.
        """
        url = f"{self.base_url}{path}"
        self._log_request("GET", url, params=params)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=self.headers, params=params)
                self._log_response(response)
                response.raise_for_status()
                return response.json()
        except Exception as error:
            self._handle_error(error, url)
            raise  # For type checker; _handle_error always exits

    def post(self, path: str, json_data: Optional[dict] = None) -> dict[str, Any]:
        """Make a POST request to the API.

        Args:
            path: API endpoint path
            json_data: JSON body data

        Returns:
            Parsed JSON response

        Raises:
            SystemExit: On any request error.
        """
        url = f"{self.base_url}{path}"
        self._log_request("POST", url, json=json_data)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=self.headers, json=json_data)
                self._log_response(response)
                response.raise_for_status()
                return response.json()
        except Exception as error:
            self._handle_error(error, url)
            raise


def create_client(
    base_url: Optional[str] = None,
    debug: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> SearchClient:
    """Create a configured SearchClient instance.

    Args:
        base_url: Override for the API base URL.
        debug: Enable debug logging.
        timeout: Request timeout in seconds.

    Returns:
        Configured SearchClient instance.
    """
    return SearchClient(base_url=base_url, debug=debug, timeout=timeout)
