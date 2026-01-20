"""Test fixtures for the Trioexplorer CLI."""

import pytest
import respx
from httpx import Response


@pytest.fixture
def mock_api():
    """Create a respx mock for the Search API."""
    with respx.mock(base_url="http://localhost:8001", assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def sample_search_response():
    """Sample search API response."""
    return {
        "results": [
            {
                "score": 0.85,
                "distance": 0.15,
                "keyword_score": 0.72,
                "patient_id": "P12345",
                "encounter_id": "E67890",
                "note_id": "N11111",
                "note_date": "2025-01-10",
                "note_type": "Progress Note",
                "text_full": "Patient presents with chest pain and shortness of breath.",
                "text_chunk": "chest pain and shortness of breath",
                "chunk_id": "C22222",
                "chunk_index": 0,
                "chunk_count": 3,
                "note_quality_score": 0.95,
                "chunk_quality_score": 0.88,
            },
            {
                "score": 0.72,
                "distance": 0.28,
                "keyword_score": 0.65,
                "patient_id": "P12346",
                "encounter_id": "E67891",
                "note_id": "N11112",
                "note_date": "2025-01-09",
                "note_type": "Discharge Summary",
                "text_full": "Diagnosis: Acute chest pain, ruled out MI.",
                "text_chunk": "Acute chest pain, ruled out MI",
                "chunk_id": "C22223",
                "chunk_index": 1,
                "chunk_count": 5,
                "note_quality_score": 0.90,
                "chunk_quality_score": 0.85,
            },
        ],
        "metadata": {
            "total_results": 2,
            "exact_match_count": 15,
            "semantic_match_count": 20,
            "unique_patients": 2,
            "unique_encounters": 2,
            "unique_notes": 2,
            "search_type": "hybrid",
            "reranked": True,
            "query": "chest pain",
        },
    }


@pytest.fixture
def sample_history_response():
    """Sample search history list response."""
    return {
        "items": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "api_key_id": "key123",
                "user_id": "user@example.com",
                "search_type": "hybrid",
                "query": "chest pain",
                "request_payload": {"query": "chest pain", "k": 10},
                "response_payload": {"results": [], "metadata": {}},
                "result_count": 10,
                "duration_ms": 150,
                "status_code": 200,
                "created_at": "2025-01-10T10:30:00Z",
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "api_key_id": "key123",
                "user_id": "user@example.com",
                "search_type": "semantic",
                "query": "diabetes mellitus",
                "request_payload": {"query": "diabetes mellitus", "k": 20},
                "response_payload": {"results": [], "metadata": {}},
                "result_count": 20,
                "duration_ms": 200,
                "status_code": 200,
                "created_at": "2025-01-10T09:15:00Z",
            },
        ],
        "total_count": 2,
        "page": 1,
        "page_size": 20,
        "has_more": False,
    }


@pytest.fixture
def sample_cohorts_response():
    """Sample indexed cohorts response."""
    return {
        "items": [
            {
                "cohort_id": "123",
                "cohort_name": "Diabetes Study",
                "namespace": "cohort-123-model-slug",
                "chunk_count": 50000,
                "index_status": "ready",
            },
            {
                "cohort_id": "456",
                "cohort_name": "Cardiac Cohort",
                "namespace": "cohort-456-model-slug",
                "chunk_count": 75000,
                "index_status": "ready",
            },
        ],
        "total_count": 2,
    }


@pytest.fixture
def sample_notetypes_response():
    """Sample note types response."""
    return {
        "items": [
            {
                "id": "uuid1",
                "note_type": "Progress Note",
                "first_seen_at": "2024-01-01T00:00:00Z",
                "last_seen_at": "2025-01-10T00:00:00Z",
                "note_count": 10000,
            },
            {
                "id": "uuid2",
                "note_type": "Discharge Summary",
                "first_seen_at": "2024-01-01T00:00:00Z",
                "last_seen_at": "2025-01-10T00:00:00Z",
                "note_count": 5000,
            },
        ],
        "total_count": 2,
    }


@pytest.fixture
def sample_stats_response():
    """Sample search history stats response."""
    return {
        "total_searches": 100,
        "unique_queries": 45,
        "avg_result_count": 12.5,
        "avg_duration_ms": 175.0,
        "searches_by_type": {
            "hybrid": 60,
            "semantic": 30,
            "keyword": 10,
        },
        "date_range": {
            "earliest": "2025-01-01T00:00:00Z",
            "latest": "2025-01-10T23:59:59Z",
        },
    }


@pytest.fixture
def env_with_api_key(monkeypatch):
    """Set up environment with API key."""
    monkeypatch.setenv("TRIOEXPLORER_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("TRIOEXPLORER_API_URL", "http://localhost:8001")


@pytest.fixture
def env_without_api_key(monkeypatch):
    """Set up environment without API key."""
    monkeypatch.delenv("TRIOEXPLORER_API_KEY", raising=False)
    monkeypatch.setenv("TRIOEXPLORER_API_URL", "http://localhost:8001")
