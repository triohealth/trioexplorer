"""Output formatters for the Trioexplorer CLI."""

import csv
import io
import json
from typing import Any, Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

# Default column widths
DEFAULT_TEXT_WIDTH = 80
SCORE_WIDTH = 8


def format_score(score: Optional[float], style: str = "yellow") -> str:
    """Format a score value with color coding."""
    if score is None:
        return "-"
    return f"{score:.4f}"


def color_score(score: Optional[float]) -> Text:
    """Create a color-coded score text based on value."""
    if score is None:
        return Text("-", style="dim")

    if score >= 0.8:
        style = "green"
    elif score >= 0.5:
        style = "yellow"
    else:
        style = "red"

    return Text(f"{score:.4f}", style=style)


def truncate_text(text: Optional[str], max_length: int = DEFAULT_TEXT_WIDTH) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def output_json(data: Any) -> None:
    """Output data as formatted JSON."""
    print(json.dumps(data, indent=2, default=str))


def output_csv(data: list[dict], fields: Optional[list[str]] = None) -> None:
    """Output data as CSV.

    Args:
        data: List of dictionaries to output.
        fields: Optional list of fields to include. If None, uses all keys from first row.
    """
    if not data:
        print("")
        return

    if fields is None:
        fields = list(data[0].keys())

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in data:
        # Convert any non-string values to strings
        writer.writerow({k: str(v) if v is not None else "" for k, v in row.items()})

    print(output.getvalue().rstrip())


def output_search_table(
    results: list[dict],
    metadata: dict,
    full_text: bool = False,
    text_width: int = DEFAULT_TEXT_WIDTH,
) -> None:
    """Output search results as a formatted table.

    Args:
        results: List of search result dictionaries.
        metadata: Search metadata dictionary.
        full_text: If True, show full note text instead of chunk.
        text_width: Maximum width for text columns.
    """
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    table = Table(
        title=f"Search Results ({metadata.get('total_results', len(results))} results)",
        show_header=True,
        header_style="bold cyan",
    )

    # Define columns
    table.add_column("#", style="dim", width=4)
    table.add_column("Score", justify="right", width=SCORE_WIDTH)
    table.add_column("Patient", width=12)
    table.add_column("Encounter", width=12)
    table.add_column("Note Type", width=20)
    table.add_column("Date", width=12)
    table.add_column("Text", width=text_width, overflow="fold")

    for idx, result in enumerate(results, 1):
        score = result.get("score")
        text_field = "text_full" if full_text else "text_chunk"
        text = truncate_text(result.get(text_field, ""), text_width)

        table.add_row(
            str(idx),
            format_score(score),
            str(result.get("patient_id", ""))[:12],
            str(result.get("encounter_id", ""))[:12],
            truncate_text(result.get("note_type", ""), 20),
            str(result.get("note_date", ""))[:10],
            text,
        )

    console.print(table)

    # Print metadata footer
    console.print()
    meta_parts = []
    if metadata.get("unique_patients"):
        meta_parts.append(f"Patients: {metadata['unique_patients']}")
    if metadata.get("unique_encounters"):
        meta_parts.append(f"Encounters: {metadata['unique_encounters']}")
    if metadata.get("unique_notes"):
        meta_parts.append(f"Notes: {metadata['unique_notes']}")
    if metadata.get("search_type"):
        meta_parts.append(f"Type: {metadata['search_type']}")
    if metadata.get("reranked") is not None:
        meta_parts.append(f"Reranked: {'yes' if metadata['reranked'] else 'no'}")

    if meta_parts:
        console.print(f"[dim]{' | '.join(meta_parts)}[/dim]")


def output_search_csv(results: list[dict]) -> None:
    """Output search results as CSV with appropriate fields."""
    fields = [
        "score",
        "distance",
        "keyword_score",
        "patient_id",
        "encounter_id",
        "note_id",
        "note_date",
        "note_type",
        "text_chunk",
        "chunk_id",
        "chunk_index",
        "chunk_count",
        "note_quality_score",
        "chunk_quality_score",
    ]
    output_csv(results, fields)


def output_history_table(
    items: list[dict],
    total_count: int,
    page: int,
    page_size: int,
    has_more: bool,
) -> None:
    """Output search history as a formatted table.

    Args:
        items: List of history entry dictionaries.
        total_count: Total number of matching entries.
        page: Current page number.
        page_size: Number of items per page.
        has_more: Whether there are more results.
    """
    if not items:
        console.print("[yellow]No search history found.[/yellow]")
        return

    table = Table(
        title=f"Search History (Page {page}, {total_count} total)",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("ID", width=36)
    table.add_column("Type", width=10)
    table.add_column("Query", width=40)
    table.add_column("Results", justify="right", width=8)
    table.add_column("Duration", justify="right", width=10)
    table.add_column("Date", width=20)

    for item in items:
        duration = item.get("duration_ms")
        duration_str = f"{duration}ms" if duration else "-"

        table.add_row(
            item.get("id", "")[:36],
            item.get("search_type", ""),
            truncate_text(item.get("query", ""), 40),
            str(item.get("result_count", 0)),
            duration_str,
            str(item.get("created_at", ""))[:19],
        )

    console.print(table)

    if has_more:
        console.print(f"[dim]Page {page} of {(total_count + page_size - 1) // page_size}. Use --page to see more.[/dim]")


def output_history_csv(items: list[dict]) -> None:
    """Output search history as CSV."""
    fields = [
        "id",
        "search_type",
        "query",
        "result_count",
        "duration_ms",
        "status_code",
        "user_id",
        "created_at",
    ]
    output_csv(items, fields)


def output_cohorts_table(items: list[dict], total_count: int) -> None:
    """Output indexed cohorts as a formatted table."""
    if not items:
        console.print("[yellow]No indexed cohorts found.[/yellow]")
        return

    table = Table(
        title=f"Indexed Cohorts ({total_count} total)",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Cohort ID", width=20)
    table.add_column("Name", width=40)
    table.add_column("Chunks", justify="right", width=12)
    table.add_column("Status", width=12)

    for item in items:
        table.add_row(
            str(item.get("cohort_id", "")),
            truncate_text(item.get("cohort_name", "-"), 40),
            str(item.get("chunk_count", 0)),
            item.get("index_status", "-"),
        )

    console.print(table)


def output_cohorts_csv(items: list[dict]) -> None:
    """Output indexed cohorts as CSV."""
    fields = ["cohort_id", "cohort_name", "namespace", "chunk_count", "index_status"]
    output_csv(items, fields)


def output_notetypes_table(items: list[dict], total_count: int) -> None:
    """Output note types as a formatted table."""
    if not items:
        console.print("[yellow]No note types found.[/yellow]")
        return

    table = Table(
        title=f"Note Types ({total_count} total)",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Note Type", width=50)
    table.add_column("Count", justify="right", width=12)
    table.add_column("First Seen", width=20)
    table.add_column("Last Seen", width=20)

    for item in items:
        table.add_row(
            truncate_text(item.get("note_type", ""), 50),
            str(item.get("note_count", 0)),
            str(item.get("first_seen_at", ""))[:10],
            str(item.get("last_seen_at", ""))[:10],
        )

    console.print(table)


def output_notetypes_csv(items: list[dict]) -> None:
    """Output note types as CSV."""
    fields = ["id", "note_type", "note_count", "first_seen_at", "last_seen_at"]
    output_csv(items, fields)


def output_stats_table(stats: dict) -> None:
    """Output search history stats as a formatted display."""
    console.print("[bold cyan]Search History Statistics[/bold cyan]")
    console.print()

    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total Searches", str(stats.get("total_searches", 0)))
    table.add_row("Unique Queries", str(stats.get("unique_queries", 0)))
    table.add_row("Avg Results", f"{stats.get('avg_result_count', 0):.1f}")

    avg_duration = stats.get("avg_duration_ms")
    if avg_duration:
        table.add_row("Avg Duration", f"{avg_duration:.0f}ms")
    else:
        table.add_row("Avg Duration", "-")

    console.print(table)

    # Searches by type
    by_type = stats.get("searches_by_type", {})
    if by_type:
        console.print()
        console.print("[bold]By Search Type:[/bold]")
        for search_type, count in sorted(by_type.items()):
            console.print(f"  {search_type}: {count}")

    # Date range
    date_range = stats.get("date_range", {})
    if date_range:
        console.print()
        earliest = date_range.get("earliest")
        latest = date_range.get("latest")
        if earliest:
            console.print(f"[dim]Earliest: {str(earliest)[:19]}[/dim]")
        if latest:
            console.print(f"[dim]Latest: {str(latest)[:19]}[/dim]")


def output_filters_table(fields: list[dict], namespace: str) -> None:
    """Output filter fields as a formatted table."""
    if not fields:
        console.print(f"[yellow]No filter fields found for namespace '{namespace}'.[/yellow]")
        return

    table = Table(
        title=f"Filter Fields ({len(fields)} fields)",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Field Name", width=30)
    table.add_column("Category", width=20)
    table.add_column("Values", justify="right", width=10)

    for field in fields:
        table.add_row(
            field.get("field_name", ""),
            field.get("field_category", ""),
            str(field.get("value_count", 0)),
        )

    console.print(table)


def output_filter_values_table(values: list[dict], field_name: str, total_values: int) -> None:
    """Output filter values for a specific field as a formatted table."""
    if not values:
        console.print(f"[yellow]No values found for field '{field_name}'.[/yellow]")
        return

    table = Table(
        title=f"Filter Values for '{field_name}' ({total_values} total)",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Value", width=50)
    table.add_column("CUI", width=12)
    table.add_column("Count", justify="right", width=10)

    for value in values:
        table.add_row(
            truncate_text(value.get("text_value", ""), 50),
            value.get("cui", "-") or "-",
            str(value.get("occurrence_count", 0)),
        )

    console.print(table)
