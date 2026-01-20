"""List commands for the Trioexplorer CLI."""

import argparse
from typing import Callable

from ..client import SearchClient
from ..output import (
    output_json,
    output_cohorts_table,
    output_cohorts_csv,
    output_notetypes_table,
    output_notetypes_csv,
    output_history_table,
    output_history_csv,
    output_filters_table,
    output_filter_values_table,
)


def add_list_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the list command parser with subcommands."""
    list_parser = subparsers.add_parser(
        "list",
        help="List resources (cohorts, notetypes, history, filters, entities)",
        description="List various resources from the Search API.",
    )

    list_subparsers = list_parser.add_subparsers(
        dest="list_command",
        title="resources",
        description="Available resources to list",
    )

    # List cohorts
    cohorts_parser = list_subparsers.add_parser(
        "cohorts",
        help="List indexed cohorts",
    )
    cohorts_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of cohorts to return (default: 10)",
    )
    cohorts_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    # List note types
    notetypes_parser = list_subparsers.add_parser(
        "notetypes",
        help="List available note types",
    )
    notetypes_parser.add_argument(
        "--search",
        metavar="TEXT",
        help="Search note types by name",
    )
    notetypes_parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of note types to return (default: 100)",
    )
    notetypes_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Number of note types to skip (default: 0)",
    )
    notetypes_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    # List history
    history_parser = list_subparsers.add_parser(
        "history",
        help="List search history",
    )
    history_parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="Page number (default: 1)",
    )
    history_parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="Number of items per page (default: 20)",
    )
    history_parser.add_argument(
        "--user-id",
        metavar="ID",
        help="Filter by user ID",
    )
    history_parser.add_argument(
        "--type",
        dest="search_type",
        choices=["hybrid", "semantic", "keyword"],
        help="Filter by search type",
    )
    history_parser.add_argument(
        "--query",
        metavar="TEXT",
        help="Filter by query text",
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
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    # List entities
    entities_parser = list_subparsers.add_parser(
        "entities",
        help="List available entity types for filtering",
    )
    entities_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    # List filters
    filters_parser = list_subparsers.add_parser(
        "filters",
        help="List available filter fields",
    )
    filters_parser.add_argument(
        "--namespace",
        metavar="NS",
        help="search index namespace (uses default if not specified)",
    )
    filters_parser.add_argument(
        "--field",
        metavar="NAME",
        help="Get values for a specific field",
    )
    filters_parser.add_argument(
        "--category",
        choices=["entity", "assertion", "entity_assertion"],
        help="Filter by field category",
    )
    filters_parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum values per field (default: 100)",
    )
    filters_parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )


def run_list(args: argparse.Namespace, get_client: Callable[[], SearchClient]) -> None:
    """Execute the list command.

    Args:
        args: Parsed arguments.
        get_client: Factory function to create the client (deferred until needed).
    """
    if args.list_command == "cohorts":
        run_list_cohorts(get_client(), args)
    elif args.list_command == "notetypes":
        run_list_notetypes(get_client(), args)
    elif args.list_command == "history":
        run_list_history(get_client(), args)
    elif args.list_command == "entities":
        # Entities command doesn't need API access - it's static data
        run_list_entities(args)
    elif args.list_command == "filters":
        run_list_filters(get_client(), args)
    else:
        from rich.console import Console
        console = Console(stderr=True)
        console.print("[red]Please specify a resource to list: cohorts, notetypes, history, entities, filters[/red]")
        raise SystemExit(1)


def run_list_cohorts(client: SearchClient, args: argparse.Namespace) -> None:
    """List indexed cohorts."""
    params = {"limit": args.limit}
    response = client.get("/cohorts/indexed", params=params)

    items = response.get("items", [])
    total_count = response.get("total_count", len(items))

    if args.output_format == "json":
        output_json(response)
    elif args.output_format == "csv":
        output_cohorts_csv(items)
    else:
        output_cohorts_table(items, total_count)


def run_list_notetypes(client: SearchClient, args: argparse.Namespace) -> None:
    """List note types."""
    params = {
        "limit": args.limit,
        "offset": args.offset,
    }
    if args.search:
        params["search"] = args.search

    response = client.get("/note-types", params=params)

    items = response.get("items", [])
    total_count = response.get("total_count", len(items))

    if args.output_format == "json":
        output_json(response)
    elif args.output_format == "csv":
        output_notetypes_csv(items)
    else:
        output_notetypes_table(items, total_count)


def run_list_history(client: SearchClient, args: argparse.Namespace) -> None:
    """List search history."""
    params = {
        "page": args.page,
        "page-size": args.page_size,
    }
    if args.user_id:
        params["user-id"] = args.user_id
    if args.search_type:
        params["search-type"] = args.search_type
    if args.query:
        params["query"] = args.query
    if args.date_from:
        params["date-from"] = args.date_from
    if args.date_to:
        params["date-to"] = args.date_to

    response = client.get("/search-history", params=params)

    items = response.get("items", [])
    total_count = response.get("total_count", len(items))
    page = response.get("page", 1)
    page_size = response.get("page_size", 20)
    has_more = response.get("has_more", False)

    if args.output_format == "json":
        output_json(response)
    elif args.output_format == "csv":
        output_history_csv(items)
    else:
        output_history_table(items, total_count, page, page_size, has_more)


def run_list_entities(args: argparse.Namespace) -> None:
    """List available entity types for filtering.

    Note: This command does not require API access - entity types are static.
    """
    # Entity types are static - just display them
    entity_types = [
        {"name": "symptoms", "description": "Clinical symptoms (e.g., fever, cough)"},
        {"name": "diagnoses", "description": "Medical diagnoses (e.g., pneumonia, diabetes)"},
        {"name": "medications", "description": "Medications and drugs"},
        {"name": "procedures", "description": "Medical procedures"},
        {"name": "lab_tests", "description": "Laboratory tests"},
        {"name": "allergies", "description": "Allergies and sensitivities"},
        {"name": "vitals", "description": "Vital signs"},
        {"name": "anatomy", "description": "Anatomical structures"},
        {"name": "devices", "description": "Medical devices"},
        {"name": "organisms", "description": "Organisms (bacteria, viruses)"},
        {"name": "substances", "description": "Chemical substances"},
        {"name": "observations", "description": "Clinical observations"},
        {"name": "social", "description": "Social history factors"},
    ]

    assertion_types = [
        {"name": "present", "description": "Entity is present/confirmed"},
        {"name": "negated", "description": "Entity is negated/absent"},
        {"name": "historical", "description": "Entity is from patient history"},
        {"name": "hypothetical", "description": "Entity is hypothetical/possible"},
        {"name": "family", "description": "Entity relates to family history"},
    ]

    if args.output_format == "json":
        output_json({
            "entity_types": entity_types,
            "assertion_types": assertion_types,
        })
    elif args.output_format == "csv":
        from ..output import output_csv
        print("# Entity Types")
        output_csv(entity_types, ["name", "description"])
        print("\n# Assertion Types")
        output_csv(assertion_types, ["name", "description"])
    else:
        from rich.console import Console
        from rich.table import Table

        console = Console()

        # Entity types table
        entity_table = Table(title="Entity Types", show_header=True, header_style="bold cyan")
        entity_table.add_column("Name", width=15)
        entity_table.add_column("Description", width=50)
        for entity in entity_types:
            entity_table.add_row(entity["name"], entity["description"])
        console.print(entity_table)

        console.print()

        # Assertion types table
        assertion_table = Table(title="Assertion Types", show_header=True, header_style="bold cyan")
        assertion_table.add_column("Name", width=15)
        assertion_table.add_column("Description", width=50)
        for assertion in assertion_types:
            assertion_table.add_row(assertion["name"], assertion["description"])
        console.print(assertion_table)

        console.print()
        console.print("[dim]Combine entity and assertion types in filters like: symptoms_present, diagnoses_negated[/dim]")


def run_list_filters(client: SearchClient, args: argparse.Namespace) -> None:
    """List available filter fields and values."""
    namespace = args.namespace or "default"

    if args.field:
        # Get values for a specific field
        params = {"limit": args.limit}
        path = f"/namespaces/{namespace}/filter-values/{args.field}"
        response = client.get(path, params=params)

        values = response.get("values", [])
        total_values = response.get("total_values", len(values))

        if args.output_format == "json":
            output_json(response)
        elif args.output_format == "csv":
            from ..output import output_csv
            output_csv(values, ["text_value", "cui", "occurrence_count"])
        else:
            output_filter_values_table(values, args.field, total_values)
    else:
        # Get field metadata
        params = {}
        if args.category:
            params["field_category"] = args.category

        path = f"/namespaces/{namespace}/filter-fields"
        response = client.get(path, params=params)

        fields = response.get("fields", [])

        if args.output_format == "json":
            output_json(response)
        elif args.output_format == "csv":
            from ..output import output_csv
            output_csv(fields, ["field_name", "field_category", "value_count"])
        else:
            output_filters_table(fields, namespace)
