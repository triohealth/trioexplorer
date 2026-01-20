"""History commands for the Trioexplorer CLI."""

import argparse

from ..client import SearchClient
from ..output import output_json


def add_history_parsers(subparsers: argparse._SubParsersAction) -> None:
    """Add the get history command parser."""
    get_parser = subparsers.add_parser(
        "get",
        help="Get a specific resource by ID",
        description="Get details of a specific resource by ID.",
    )

    get_subparsers = get_parser.add_subparsers(
        dest="get_command",
        title="resources",
        description="Available resources to get",
    )

    # Get history entry by ID
    history_parser = get_subparsers.add_parser(
        "history",
        help="Get a search history entry by ID",
    )
    history_parser.add_argument(
        "history_id",
        help="Search history entry ID",
    )
    history_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )


def run_get_history(client: SearchClient, args: argparse.Namespace) -> None:
    """Execute the get command."""
    if args.get_command == "history":
        run_get_history_entry(client, args)
    else:
        from rich.console import Console
        console = Console(stderr=True)
        console.print("[red]Please specify a resource to get: history[/red]")
        raise SystemExit(1)


def run_get_history_entry(client: SearchClient, args: argparse.Namespace) -> None:
    """Get a specific search history entry."""
    response = client.get(f"/search-history/{args.history_id}")

    if args.output_format == "json":
        output_json(response)
    else:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table

        console = Console()

        # Basic info panel
        info_table = Table(show_header=False, box=None)
        info_table.add_column("Field", style="bold")
        info_table.add_column("Value")

        info_table.add_row("ID", response.get("id", ""))
        info_table.add_row("Type", response.get("search_type", ""))
        info_table.add_row("Query", response.get("query", ""))
        info_table.add_row("Results", str(response.get("result_count", 0)))

        duration = response.get("duration_ms")
        info_table.add_row("Duration", f"{duration}ms" if duration else "-")

        info_table.add_row("Status", str(response.get("status_code", "")))
        info_table.add_row("User ID", response.get("user_id", "-") or "-")
        info_table.add_row("Created", str(response.get("created_at", ""))[:19])

        console.print(Panel(info_table, title="Search History Entry", border_style="cyan"))

        # Request payload
        request_payload = response.get("request_payload", {})
        if request_payload:
            console.print()
            console.print("[bold]Request Payload:[/bold]")
            import json
            console.print(json.dumps(request_payload, indent=2))

        # Response metadata (not full results)
        response_payload = response.get("response_payload", {})
        if response_payload:
            metadata = response_payload.get("metadata", {})
            if metadata:
                console.print()
                console.print("[bold]Response Metadata:[/bold]")
                import json
                console.print(json.dumps(metadata, indent=2))

        # Error message if present
        error_message = response.get("error_message")
        if error_message:
            console.print()
            console.print(f"[red]Error: {error_message}[/red]")
