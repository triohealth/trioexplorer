"""Search command for the Trioexplorer CLI."""

import argparse
import json
import sys
from typing import Any

from rich.console import Console

from ..client import SearchClient
from ..output import (
    output_json,
    output_search_csv,
    output_search_table,
)

console = Console(stderr=True)


def str_to_bool(value: str) -> bool:
    """Convert string to boolean for argparse."""
    if value.lower() in ("true", "yes", "1"):
        return True
    elif value.lower() in ("false", "no", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def add_search_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the search command parser."""
    parser = subparsers.add_parser(
        "search",
        help="Search clinical notes",
        description="Search clinical notes with various filters and options.",
    )

    parser.add_argument(
        "query",
        help="Search query text",
    )

    parser.add_argument(
        "-k",
        type=int,
        default=10,
        metavar="NUM",
        help="Number of results to return (1-300, default: 10)",
    )

    parser.add_argument(
        "-t", "--type",
        dest="search_type",
        choices=["hybrid", "semantic", "keyword"],
        default="hybrid",
        help="Search type (default: hybrid)",
    )

    parser.add_argument(
        "-d", "--distinct",
        choices=["encounter", "patient", "note", "none"],
        default="encounter",
        help="De-duplication mode (default: encounter)",
    )

    parser.add_argument(
        "-c", "--cohort-ids",
        metavar="IDS",
        help="Comma-separated cohort IDs",
    )

    parser.add_argument(
        "--rerank",
        type=str_to_bool,
        default=True,
        metavar="BOOL",
        help="Apply Cohere reranking (default: true)",
    )

    parser.add_argument(
        "--vector-weight",
        type=float,
        default=0.7,
        metavar="FLOAT",
        help="Vector weight in fusion (0.0-1.0, default: 0.7)",
    )

    parser.add_argument(
        "--top-k-retrieval",
        type=int,
        metavar="NUM",
        help="Pre-reranking retrieval count",
    )

    parser.add_argument(
        "--distance-threshold",
        type=float,
        default=0.7,
        metavar="FLOAT",
        help="Cosine distance cutoff (0.0-2.0, default: 0.7)",
    )

    parser.add_argument(
        "--chunk-multiplier",
        type=float,
        default=2.0,
        metavar="FLOAT",
        help="Initial retrieval multiplier (1.0-5.0, default: 2.0)",
    )

    parser.add_argument(
        "--min-quality-score",
        type=float,
        metavar="FLOAT",
        help="Minimum note quality score (0.0-1.0)",
    )

    parser.add_argument(
        "--min-chunk-quality-score",
        type=float,
        metavar="FLOAT",
        help="Minimum chunk quality score (0.0-1.0)",
    )

    parser.add_argument(
        "-f", "--filters",
        metavar="JSON",
        help="search index filters (JSON format)",
    )

    parser.add_argument(
        "-e", "--entity-filters",
        metavar="JSON",
        help="Entity/assertion filters (JSON format)",
    )

    parser.add_argument(
        "-o", "--format",
        dest="output_format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    parser.add_argument(
        "--full-text",
        action="store_true",
        help="Show full note text instead of chunk",
    )


def validate_json_arg(value: str, arg_name: str) -> Any:
    """Validate and parse a JSON argument."""
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON for {arg_name}: {e}[/red]")
        sys.exit(1)


def run_search(client: SearchClient, args: argparse.Namespace) -> None:
    """Execute the search command."""
    # Validate JSON arguments
    filters = None
    if args.filters:
        filters = validate_json_arg(args.filters, "--filters")

    entity_filters = None
    if args.entity_filters:
        entity_filters = validate_json_arg(args.entity_filters, "--entity-filters")

    # Build query parameters
    params = {
        "query": args.query,
        "search-type": args.search_type,
        "k": args.k,
        "distinct": args.distinct,
        "rerank": str(args.rerank).lower(),
        "vector_weight": args.vector_weight,
        "distance_threshold": args.distance_threshold,
        "chunk-multiplier": args.chunk_multiplier,
    }

    # Add optional parameters
    if args.cohort_ids:
        params["cohort-ids"] = args.cohort_ids

    if args.top_k_retrieval:
        params["top_k_retrieval"] = args.top_k_retrieval

    if args.min_quality_score is not None:
        params["min-quality-score"] = args.min_quality_score

    if args.min_chunk_quality_score is not None:
        params["min-chunk-quality-score"] = args.min_chunk_quality_score

    if filters:
        params["filters"] = json.dumps(filters)

    if entity_filters:
        params["entity-filters"] = json.dumps(entity_filters)

    # Make the request
    response = client.get("/search", params=params)

    # Output results
    results = response.get("results", [])
    metadata = response.get("metadata", {})

    if args.output_format == "json":
        output_json(response)
    elif args.output_format == "csv":
        output_search_csv(results)
    else:
        output_search_table(results, metadata, full_text=args.full_text)
