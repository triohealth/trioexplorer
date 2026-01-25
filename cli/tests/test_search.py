"""Tests for the search command."""

import argparse
import json
import pytest
from httpx import Response

from trioexplorer.client import create_client
from trioexplorer.commands.search import build_filters_from_args


class TestSearchCommand:
    """Tests for the search command."""

    def test_basic_search(self, mock_api, sample_search_response, env_with_api_key):
        """Test basic search request."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get("/search", params={"query": "chest pain"})

        assert response["results"] is not None
        assert len(response["results"]) == 2
        assert response["metadata"]["total_results"] == 2

    def test_search_with_type(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with search type parameter."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get(
            "/search",
            params={"query": "chest pain", "search-type": "semantic"},
        )

        assert response["results"] is not None

    def test_search_with_cohort_ids(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with cohort filtering."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get(
            "/search",
            params={"query": "diabetes", "cohort-ids": "123,456"},
        )

        assert response["results"] is not None

    def test_search_with_quality_filters(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with quality score filters."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get(
            "/search",
            params={
                "query": "cardiac",
                "min-quality-score": 0.8,
                "min-chunk-quality-score": 0.7,
            },
        )

        assert response["results"] is not None

    def test_search_with_advanced_params(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with advanced tuning parameters."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get(
            "/search",
            params={
                "query": "pneumonia",
                "rerank": "false",
                "vector_weight": 0.5,
                "distance_threshold": 0.6,
                "chunk-multiplier": 3.0,
                "top_k_retrieval": 500,
            },
        )

        assert response["results"] is not None

    def test_search_with_filters(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with metadata filters."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        filters = [["note_type", "Eq", "DISCHARGE SUMMARY"]]
        client = create_client()
        response = client.get(
            "/search",
            params={
                "query": "sepsis",
                "filters": json.dumps(filters),
            },
        )

        assert response["results"] is not None

    def test_search_with_entity_filters(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with entity filters."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        entity_filters = {"medication": {"present": True}}
        client = create_client()
        response = client.get(
            "/search",
            params={
                "query": "medications",
                "entity-filters": json.dumps(entity_filters),
            },
        )

        assert response["results"] is not None

    def test_search_with_k_parameter(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with custom k parameter."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        client = create_client()
        response = client.get(
            "/search",
            params={"query": "chest pain", "k": 20},
        )

        assert response["results"] is not None

    def test_search_with_distinct_mode(self, mock_api, sample_search_response, env_with_api_key):
        """Test search with different distinct modes."""
        mock_api.get("/search").mock(
            return_value=Response(200, json=sample_search_response)
        )

        for mode in ["encounter", "patient", "note", "none"]:
            client = create_client()
            response = client.get(
                "/search",
                params={"query": "chest pain", "distinct": mode},
            )
            assert response["results"] is not None


class TestSearchErrors:
    """Tests for search error handling."""

    def test_search_auth_error(self, mock_api, env_with_api_key):
        """Test handling of authentication errors."""
        mock_api.get("/search").mock(
            return_value=Response(401, json={"detail": "Invalid API key"})
        )

        client = create_client()
        with pytest.raises(SystemExit):
            client.get("/search", params={"query": "test"})

    def test_search_forbidden_error(self, mock_api, env_with_api_key):
        """Test handling of authorization errors."""
        mock_api.get("/search").mock(
            return_value=Response(403, json={"detail": "Access denied"})
        )

        client = create_client()
        with pytest.raises(SystemExit):
            client.get("/search", params={"query": "test"})

    def test_search_not_found_error(self, mock_api, env_with_api_key):
        """Test handling of not found errors."""
        mock_api.get("/search").mock(
            return_value=Response(404, json={"detail": "Cohort not found"})
        )

        client = create_client()
        with pytest.raises(SystemExit):
            client.get("/search", params={"query": "test"})

    def test_missing_api_key(self, env_without_api_key):
        """Test error when API key is not set."""
        with pytest.raises(SystemExit) as exc_info:
            create_client()

        assert "TRIOEXPLORER_API_KEY" in str(exc_info.value)


class TestBuildFiltersFromArgs:
    """Tests for the build_filters_from_args function."""

    def _make_args(self, **kwargs):
        """Create an argparse.Namespace with default values."""
        defaults = {
            "patient_id": None,
            "encounter_id": None,
            "note_types": None,
            "date_from": None,
            "date_to": None,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_no_filters(self):
        """Test with no filter arguments."""
        args = self._make_args()
        result = build_filters_from_args(args, None)
        assert result is None

    def test_patient_id_filter(self):
        """Test patient_id filter construction."""
        args = self._make_args(patient_id="001EFCDE-62D9-42A0-B184-3E3C732EBDA5")
        result = build_filters_from_args(args, None)
        assert result == ["patient_id", "Eq", "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"]

    def test_encounter_id_filter(self):
        """Test encounter_id filter construction."""
        args = self._make_args(encounter_id="ABC12345-6789-0DEF-GHIJ")
        result = build_filters_from_args(args, None)
        assert result == ["encounter_id", "Eq", "ABC12345-6789-0DEF-GHIJ"]

    def test_single_note_type_filter(self):
        """Test single note type filter construction."""
        args = self._make_args(note_types="Progress Note")
        result = build_filters_from_args(args, None)
        assert result == ["note_type", "Eq", "Progress Note"]

    def test_multiple_note_types_filter(self):
        """Test multiple note types filter construction."""
        args = self._make_args(note_types="Progress Note,Discharge Summary")
        result = build_filters_from_args(args, None)
        assert result == ["note_type", "In", ["Progress Note", "Discharge Summary"]]

    def test_date_from_filter(self):
        """Test date_from filter construction."""
        args = self._make_args(date_from="2025-01-01")
        result = build_filters_from_args(args, None)
        assert result == ["note_date", "Gte", "2025-01-01"]

    def test_date_to_filter(self):
        """Test date_to filter construction."""
        args = self._make_args(date_to="2025-12-31")
        result = build_filters_from_args(args, None)
        assert result == ["note_date", "Lte", "2025-12-31"]

    def test_combined_filters(self):
        """Test multiple filter arguments combined with And."""
        args = self._make_args(
            patient_id="001EFCDE-62D9-42A0-B184-3E3C732EBDA5",
            date_from="2025-01-01",
            note_types="Progress Note",
        )
        result = build_filters_from_args(args, None)
        assert result == [
            "And",
            [
                ["patient_id", "Eq", "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"],
                ["note_type", "Eq", "Progress Note"],
                ["note_date", "Gte", "2025-01-01"],
            ],
        ]

    def test_merge_with_user_filters(self):
        """Test merging CLI filters with user-provided filters."""
        args = self._make_args(patient_id="001EFCDE-62D9-42A0-B184-3E3C732EBDA5")
        user_filters = ["cohort_ids", "Contains", 123]
        result = build_filters_from_args(args, user_filters)
        assert result == [
            "And",
            [
                ["patient_id", "Eq", "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"],
                ["cohort_ids", "Contains", 123],
            ],
        ]

    def test_user_filters_only(self):
        """Test with only user-provided filters."""
        args = self._make_args()
        user_filters = ["note_type", "Eq", "Discharge Summary"]
        result = build_filters_from_args(args, user_filters)
        assert result == ["note_type", "Eq", "Discharge Summary"]
