"""Main entry point for the Trioexplorer CLI."""

import argparse
import sys

from . import __version__
from .client import create_client, SearchClient
from .commands.search import add_search_parser, run_search
from .commands.list import add_list_parser, run_list
from .commands.history import add_history_parsers, run_get_history
from .commands.stats import add_stats_parser, run_stats


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="trioexplorer",
        description="Command-line interface for the Search API",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable request/response logging",
    )

    parser.add_argument(
        "--api-url",
        metavar="URL",
        help="Override TRIOEXPLORER_API_URL",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands",
    )

    # Add command parsers
    add_search_parser(subparsers)
    add_list_parser(subparsers)
    add_history_parsers(subparsers)
    add_stats_parser(subparsers)

    return parser


def get_client(args: argparse.Namespace) -> SearchClient:
    """Create the client with global options (deferred creation)."""
    return create_client(
        base_url=args.api_url,
        debug=args.debug,
    )


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Route to appropriate command handler
    # Client creation is deferred to commands that need it
    if args.command == "search":
        run_search(get_client(args), args)
    elif args.command == "list":
        run_list(args, lambda: get_client(args))
    elif args.command == "get":
        run_get_history(get_client(args), args)
    elif args.command == "stats":
        run_stats(get_client(args), args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
