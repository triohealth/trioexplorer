"""Tests for output formatters."""

import io
import json
import sys
import pytest

from trioexplorer.output import (
    format_score,
    truncate_text,
    output_json,
    output_csv,
    output_search_csv,
    output_history_csv,
    output_cohorts_csv,
    output_notetypes_csv,
)


class TestScoreFormatting:
    """Tests for score formatting."""

    def test_format_score_normal(self):
        """Test formatting a normal score."""
        assert format_score(0.8523) == "0.8523"

    def test_format_score_zero(self):
        """Test formatting zero score."""
        assert format_score(0.0) == "0.0000"

    def test_format_score_one(self):
        """Test formatting score of 1."""
        assert format_score(1.0) == "1.0000"

    def test_format_score_none(self):
        """Test formatting None score."""
        assert format_score(None) == "-"


class TestTextTruncation:
    """Tests for text truncation."""

    def test_truncate_short_text(self):
        """Test that short text is not truncated."""
        text = "Short text"
        assert truncate_text(text, 50) == text

    def test_truncate_long_text(self):
        """Test that long text is truncated with ellipsis."""
        text = "This is a very long text that should be truncated"
        result = truncate_text(text, 20)
        assert len(result) == 20
        assert result.endswith("...")

    def test_truncate_exact_length(self):
        """Test text at exact max length."""
        text = "Exactly twenty chars"
        assert truncate_text(text, 20) == text

    def test_truncate_none(self):
        """Test truncating None."""
        assert truncate_text(None) == ""

    def test_truncate_empty(self):
        """Test truncating empty string."""
        assert truncate_text("") == ""


class TestJsonOutput:
    """Tests for JSON output."""

    def test_output_json(self, capsys):
        """Test JSON output formatting."""
        data = {"key": "value", "number": 42}
        output_json(data)
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["key"] == "value"
        assert parsed["number"] == 42

    def test_output_json_nested(self, capsys):
        """Test JSON output with nested data."""
        data = {
            "results": [{"id": 1}, {"id": 2}],
            "metadata": {"count": 2},
        }
        output_json(data)
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert len(parsed["results"]) == 2


class TestCsvOutput:
    """Tests for CSV output."""

    def test_output_csv_basic(self, capsys):
        """Test basic CSV output."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        output_csv(data)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 3  # header + 2 rows
        assert "name" in lines[0]
        assert "Alice" in lines[1]
        assert "Bob" in lines[2]

    def test_output_csv_with_fields(self, capsys):
        """Test CSV output with specific fields."""
        data = [
            {"name": "Alice", "age": 30, "city": "NYC"},
            {"name": "Bob", "age": 25, "city": "LA"},
        ]
        output_csv(data, fields=["name", "city"])
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert "name" in lines[0]
        assert "city" in lines[0]
        assert "age" not in lines[0]

    def test_output_csv_empty(self, capsys):
        """Test CSV output with empty data."""
        output_csv([])
        captured = capsys.readouterr()
        assert captured.out.strip() == ""

    def test_output_csv_with_none_values(self, capsys):
        """Test CSV output handles None values."""
        data = [
            {"name": "Alice", "score": None},
            {"name": "Bob", "score": 0.5},
        ]
        output_csv(data)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 3


class TestSearchCsvOutput:
    """Tests for search-specific CSV output."""

    def test_output_search_csv(self, capsys):
        """Test search results CSV output."""
        results = [
            {
                "score": 0.85,
                "distance": 0.15,
                "keyword_score": 0.72,
                "patient_id": "P12345",
                "encounter_id": "E67890",
                "note_id": "N11111",
                "note_date": "2025-01-10",
                "note_type": "Progress Note",
                "text_chunk": "chest pain",
                "chunk_id": "C22222",
                "chunk_index": 0,
                "chunk_count": 3,
                "note_quality_score": 0.95,
                "chunk_quality_score": 0.88,
            }
        ]
        output_search_csv(results)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2  # header + 1 row
        assert "score" in lines[0]
        assert "patient_id" in lines[0]


class TestHistoryCsvOutput:
    """Tests for history-specific CSV output."""

    def test_output_history_csv(self, capsys):
        """Test history CSV output."""
        items = [
            {
                "id": "uuid1",
                "search_type": "hybrid",
                "query": "chest pain",
                "result_count": 10,
                "duration_ms": 150,
                "status_code": 200,
                "user_id": "user@example.com",
                "created_at": "2025-01-10T10:30:00Z",
            }
        ]
        output_history_csv(items)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2
        assert "search_type" in lines[0]
        assert "query" in lines[0]


class TestCohortsCsvOutput:
    """Tests for cohorts-specific CSV output."""

    def test_output_cohorts_csv(self, capsys):
        """Test cohorts CSV output."""
        items = [
            {
                "cohort_id": "123",
                "cohort_name": "Test Cohort",
                "namespace": "cohort-123-model",
                "chunk_count": 50000,
                "index_status": "ready",
            }
        ]
        output_cohorts_csv(items)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2
        assert "cohort_id" in lines[0]
        assert "cohort_name" in lines[0]


class TestNotetypesCsvOutput:
    """Tests for notetypes-specific CSV output."""

    def test_output_notetypes_csv(self, capsys):
        """Test notetypes CSV output."""
        items = [
            {
                "id": "uuid1",
                "note_type": "Progress Note",
                "note_count": 10000,
                "first_seen_at": "2024-01-01",
                "last_seen_at": "2025-01-10",
            }
        ]
        output_notetypes_csv(items)
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2
        assert "note_type" in lines[0]
        assert "note_count" in lines[0]
