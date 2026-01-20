"""Stats commands for the Trioexplorer CLI."""

import argparse

from ..client import SearchClient
from ..output import output_json, output_stats_table


def add_stats_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the stats command parser."""
    stats_parser = subparsers.add_parser(
        "stats",
        help="Get statistics",
        description="Get statistics for various resources.",
    )

    stats_subparsers = stats_parser.add_subparsers(
        dest="stats_command",
        title="resources",
        description="Available statistics",
    )

    # History stats
    history_parser = stats_subparsers.add_parser(
        "history",
        help="Get search history statistics",
    )
    history_parser.add_argument(
        "--date-from",
        metavar="DATE",
        help="Filter from date (ISO format)",
    )
    history_parser.add_argument(
        "--date-to",
        metavar="DATE",
        help="Filter to date (ISO format)",
    )
    history_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )


def run_stats(client: SearchClient, args: argparse.Namespace) -> None:
    """Execute the stats command."""
    if args.stats_command == "history":
        run_stats_history(client, args)
    else:
        from rich.console import Console
        console = Console(stderr=True)
        console.print("[red]Please specify a stats type: history[/red]")
        raise SystemExit(1)


def run_stats_history(client: SearchClient, args: argparse.Namespace) -> None:
    """Get search history statistics."""
    params = {}
    if args.date_from:
        params["date-from"] = args.date_from
    if args.date_to:
        params["date-to"] = args.date_to

    response = client.get("/search-history/stats/summary", params=params)

    if args.output_format == "json":
        output_json(response)
    else:
        output_stats_table(response)
