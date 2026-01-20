"""Tests for list commands."""

import pytest
from httpx import Response

from trioexplorer.client import create_client


class TestListCohorts:
    """Tests for the list cohorts command."""

    def test_list_cohorts(self, mock_api, sample_cohorts_response, env_with_api_key):
        """Test listing indexed cohorts."""
        mock_api.get("/cohorts/indexed").mock(
            return_value=Response(200, json=sample_cohorts_response)
        )

        client = create_client()
        response = client.get("/cohorts/indexed", params={"limit": 10})

        assert response["items"] is not None
        assert len(response["items"]) == 2
        assert response["total_count"] == 2

    def test_list_cohorts_with_limit(self, mock_api, sample_cohorts_response, env_with_api_key):
        """Test listing cohorts with custom limit."""
        mock_api.get("/cohorts/indexed").mock(
            return_value=Response(200, json=sample_cohorts_response)
        )

        client = create_client()
        response = client.get("/cohorts/indexed", params={"limit": 50})

        assert response["items"] is not None


class TestListNoteTypes:
    """Tests for the list notetypes command."""

    def test_list_notetypes(self, mock_api, sample_notetypes_response, env_with_api_key):
        """Test listing note types."""
        mock_api.get("/note-types").mock(
            return_value=Response(200, json=sample_notetypes_response)
        )

        client = create_client()
        response = client.get("/note-types", params={"limit": 100})

        assert response["items"] is not None
        assert len(response["items"]) == 2
        assert response["total_count"] == 2

    def test_list_notetypes_with_search(self, mock_api, sample_notetypes_response, env_with_api_key):
        """Test listing note types with search filter."""
        mock_api.get("/note-types").mock(
            return_value=Response(200, json=sample_notetypes_response)
        )

        client = create_client()
        response = client.get("/note-types", params={"search": "discharge", "limit": 100})

        assert response["items"] is not None

    def test_list_notetypes_with_pagination(self, mock_api, sample_notetypes_response, env_with_api_key):
        """Test listing note types with pagination."""
        mock_api.get("/note-types").mock(
            return_value=Response(200, json=sample_notetypes_response)
        )

        client = create_client()
        response = client.get("/note-types", params={"limit": 10, "offset": 20})

        assert response["items"] is not None


class TestListHistory:
    """Tests for the list history command."""

    def test_list_history(self, mock_api, sample_history_response, env_with_api_key):
        """Test listing search history."""
        mock_api.get("/search-history").mock(
            return_value=Response(200, json=sample_history_response)
        )

        client = create_client()
        response = client.get("/search-history", params={"page": 1, "page-size": 20})

        assert response["items"] is not None
        assert len(response["items"]) == 2
        assert response["total_count"] == 2
        assert response["page"] == 1

    def test_list_history_with_filters(self, mock_api, sample_history_response, env_with_api_key):
        """Test listing history with filters."""
        mock_api.get("/search-history").mock(
            return_value=Response(200, json=sample_history_response)
        )

        client = create_client()
        response = client.get(
            "/search-history",
            params={
                "page": 1,
                "page-size": 20,
                "user-id": "user@example.com",
                "search-type": "hybrid",
            },
        )

        assert response["items"] is not None

    def test_list_history_with_date_range(self, mock_api, sample_history_response, env_with_api_key):
        """Test listing history with date range filters."""
        mock_api.get("/search-history").mock(
            return_value=Response(200, json=sample_history_response)
        )

        client = create_client()
        response = client.get(
            "/search-history",
            params={
                "page": 1,
                "page-size": 20,
                "date-from": "2025-01-01",
                "date-to": "2025-01-31",
            },
        )

        assert response["items"] is not None

    def test_list_history_with_query_filter(self, mock_api, sample_history_response, env_with_api_key):
        """Test listing history filtered by query text."""
        mock_api.get("/search-history").mock(
            return_value=Response(200, json=sample_history_response)
        )

        client = create_client()
        response = client.get(
            "/search-history",
            params={
                "page": 1,
                "page-size": 20,
                "query": "diabetes",
            },
        )

        assert response["items"] is not None


class TestListFilters:
    """Tests for the list filters command."""

    def test_list_filter_fields(self, mock_api, env_with_api_key):
        """Test listing filter fields."""
        response_data = {
            "namespace": "global-model-slug",
            "fields": [
                {"field_name": "symptoms", "field_category": "entity", "value_count": 100},
                {"field_name": "present", "field_category": "assertion", "value_count": 50},
            ],
            "total_fields": 2,
        }
        mock_api.get("/namespaces/global-model-slug/filter-fields").mock(
            return_value=Response(200, json=response_data)
        )

        client = create_client()
        response = client.get("/namespaces/global-model-slug/filter-fields")

        assert response["fields"] is not None
        assert len(response["fields"]) == 2

    def test_list_filter_values(self, mock_api, env_with_api_key):
        """Test listing filter values for a field."""
        response_data = {
            "namespace": "global-model-slug",
            "field_name": "symptoms",
            "field_category": "entity",
            "values": [
                {"id": "uuid1", "text_value": "fever", "cui": "C0015967", "occurrence_count": 500},
                {"id": "uuid2", "text_value": "cough", "cui": "C0010200", "occurrence_count": 400},
            ],
            "total_values": 2,
        }
        mock_api.get("/namespaces/global-model-slug/filter-values/symptoms").mock(
            return_value=Response(200, json=response_data)
        )

        client = create_client()
        response = client.get(
            "/namespaces/global-model-slug/filter-values/symptoms",
            params={"limit": 100},
        )

        assert response["values"] is not None
        assert len(response["values"]) == 2
