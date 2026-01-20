"""Tests for history commands."""

import pytest
from httpx import Response

from trioexplorer.client import create_client


class TestGetHistory:
    """Tests for the get history command."""

    def test_get_history_entry(self, mock_api, env_with_api_key):
        """Test getting a specific history entry."""
        history_id = "550e8400-e29b-41d4-a716-446655440001"
        response_data = {
            "id": history_id,
            "api_key_id": "key123",
            "user_id": "user@example.com",
            "search_type": "hybrid",
            "query": "chest pain",
            "request_payload": {
                "query": "chest pain",
                "k": 10,
                "search_type": "hybrid",
            },
            "response_payload": {
                "results": [],
                "metadata": {
                    "total_results": 10,
                    "search_type": "hybrid",
                },
            },
            "result_count": 10,
            "duration_ms": 150,
            "status_code": 200,
            "error_message": None,
            "created_at": "2025-01-10T10:30:00Z",
        }
        mock_api.get(f"/search-history/{history_id}").mock(
            return_value=Response(200, json=response_data)
        )

        client = create_client()
        response = client.get(f"/search-history/{history_id}")

        assert response["id"] == history_id
        assert response["query"] == "chest pain"
        assert response["search_type"] == "hybrid"
        assert response["result_count"] == 10

    def test_get_history_entry_not_found(self, mock_api, env_with_api_key):
        """Test getting a non-existent history entry."""
        history_id = "nonexistent-id"
        mock_api.get(f"/search-history/{history_id}").mock(
            return_value=Response(404, json={"detail": "Search history entry not found"})
        )

        client = create_client()
        with pytest.raises(SystemExit):
            client.get(f"/search-history/{history_id}")

    def test_get_history_entry_with_error(self, mock_api, env_with_api_key):
        """Test getting a history entry that recorded an error."""
        history_id = "550e8400-e29b-41d4-a716-446655440002"
        response_data = {
            "id": history_id,
            "api_key_id": "key123",
            "user_id": "user@example.com",
            "search_type": "hybrid",
            "query": "invalid query",
            "request_payload": {"query": "invalid query"},
            "response_payload": {},
            "result_count": 0,
            "duration_ms": 50,
            "status_code": 400,
            "error_message": "Invalid query syntax",
            "created_at": "2025-01-10T09:00:00Z",
        }
        mock_api.get(f"/search-history/{history_id}").mock(
            return_value=Response(200, json=response_data)
        )

        client = create_client()
        response = client.get(f"/search-history/{history_id}")

        assert response["id"] == history_id
        assert response["status_code"] == 400
        assert response["error_message"] == "Invalid query syntax"


class TestHistoryStats:
    """Tests for history statistics."""

    def test_get_history_stats(self, mock_api, sample_stats_response, env_with_api_key):
        """Test getting search history stats."""
        mock_api.get("/search-history/stats/summary").mock(
            return_value=Response(200, json=sample_stats_response)
        )

        client = create_client()
        response = client.get("/search-history/stats/summary")

        assert response["total_searches"] == 100
        assert response["unique_queries"] == 45
        assert response["avg_result_count"] == 12.5
        assert response["avg_duration_ms"] == 175.0
        assert "hybrid" in response["searches_by_type"]

    def test_get_history_stats_with_date_range(self, mock_api, sample_stats_response, env_with_api_key):
        """Test getting stats with date range filter."""
        mock_api.get("/search-history/stats/summary").mock(
            return_value=Response(200, json=sample_stats_response)
        )

        client = create_client()
        response = client.get(
            "/search-history/stats/summary",
            params={
                "date-from": "2025-01-01",
                "date-to": "2025-01-31",
            },
        )

        assert response["total_searches"] is not None
