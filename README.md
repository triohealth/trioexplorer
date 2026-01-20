# Trioexplorer

A powerful hybrid search API for clinical notes, combining semantic vector search with BM25 keyword matching for comprehensive and accurate results.

> **Note:** To get an API key, contact sales@trioehealth.com

## Overview

Trioexplorer enables searching across indexed patient notes using three search modes:

| Mode | Description | Best For |
|------|-------------|----------|
| `keyword` | BM25 full-text search | Exact terms, medical codes (e.g., "ICD-10 E11.9"), specific phrases |
| `semantic` | Vector similarity search | Conceptual queries (e.g., "patient struggling with blood sugar") |
| `hybrid` | Combines both with intelligent fusion | General-purpose queries (default) |

## Example searches

Set up your environment variables:
```bash
export TRIO_API_URL="http://k8s-notesear-notesear-20ee5f12c9-4c4972a75575c8a7.elb.us-east-1.amazonaws.com:8001"
export TRIO_API_KEY="YOUR_API_KEY"
```

### 1. Global search

Search across all cohorts accessible to your API key.

```bash
curl -X GET "$TRIO_API_URL/search" \
  -H "X-API-Key: $TRIO_API_KEY" \
  -G \
  --data-urlencode "query=diabetes management" \
  --data-urlencode "k=10"
```

### 2. Cohort search (discover available cohorts)

First, list available cohorts:

```bash
curl -X GET "$TRIO_API_URL/cohorts/indexed" \
  -H "X-API-Key: $TRIO_API_KEY"
```

Then, search within specific cohorts using `cohort-ids`:

```bash
curl -X GET "$TRIO_API_URL/search" \
  -H "X-API-Key: $TRIO_API_KEY" \
  -G \
  --data-urlencode "query=diabetes management" \
  --data-urlencode "cohort-ids=123,456"
```

### 3. Patient search

Filter results to a specific patient using `patient-id`.

```bash
curl -X GET "$TRIO_API_URL/search" \
  -H "X-API-Key: $TRIO_API_KEY" \
  -G \
  --data-urlencode "query=hypertension" \
  --data-urlencode "patient-id=3638E059-DFF3-4F24-9A7F-16F9EC2AD120"
```

### 4. Date range search

Restrict search to clinical notes within a date range.

```bash
curl -X GET "$TRIO_API_URL/search" \
  -H "X-API-Key: $TRIO_API_KEY" \
  -G \
  --data-urlencode "query=post-op complications" \
  --data-urlencode "date-from=2024-01-01" \
  --data-urlencode "date-to=2024-12-31"
```

### Interactive Quickstart

See the [Getting Started Notebook](notebooks/getting_started.ipynb) for an interactive tutorial with visualizations.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/triohealth/trioexplorer/blob/main/notebooks/getting_started.ipynb)

---

## Authentication

All API requests require an `X-API-Key` header:

```
X-API-Key: ts_your_api_key_here
```


## API Reference

### Health Check

Check if the API is running.

```
GET /health
```

**Response:**
```json
{"status": "healthy"}
```

---

### List Indexed Cohorts

Discover which cohorts are available for search.

```
GET /cohorts/indexed
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Max cohorts to return (1-100) |

**Response:**
```json
{
  "items": [
    {
      "cohort_id": "123",
      "cohort_name": "Diabetes Cohort",
      "namespace": "cohort-123-nomic-embed-text",
      "chunk_count": 15000,
      "index_status": "ready"
    }
  ],
  "total_count": 5
}
```

---

### Search Notes

Search indexed patient notes with configurable modes and filters.

```
GET /search
```

#### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | **required** | Search text |
| `search-type` | string | `hybrid` | `keyword`, `semantic`, or `hybrid` |
| `k` | integer | 10 | Number of unique notes to return (1-300) |
| `cohort-ids` | string | — | Comma-separated cohort IDs to search |
| `rerank` | boolean | true | Apply semantic reranking (hybrid only) |

#### Filter Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `patient-id` | string | Filter to specific patient |
| `encounter-id` | string | Filter to specific encounter |
| `note-types` | string | Comma-separated note types (e.g., "Progress Note,Discharge Summary") |
| `date-from` | string | Filter from date (YYYY-MM-DD, inclusive) |
| `date-to` | string | Filter to date (YYYY-MM-DD, inclusive) |

#### Advanced Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vector-weight` | float | 0.7 | Weight for vector vs keyword in fusion (0.0-1.0) |
| `distance-threshold` | float | 0.7 | Max cosine distance for semantic matches (0.0-2.0) |
| `top-k-retrieval` | integer | 4×k | Max chunks to retrieve before deduplication |
| `include-noise` | boolean | false | Include notes marked as noise |
| `skip-omitted-count` | boolean | false | Skip omitted count calculation (faster) |

#### Response

```json
{
  "results": [
    {
      "score": 0.8421,
      "distance": 0.2541,
      "keyword_score": 0.0987,
      "patient_id": "3638E059-DFF3-4F24-9A7F-16F9EC2AD120",
      "encounter_id": "114C6CEB-F5B6-4E40-AED6-7ECAB80245FE",
      "note_id": "155C605A-DC6E-42C1-BC10-21FC777B429B",
      "note_date": "2025-03-04",
      "note_type": "DISCHARGE SUMMARY",
      "text_full": "... full note text ...",
      "text_chunk": "... relevant chunk matched ...",
      "chunk_id": "chunk-123",
      "chunk_index": 0,
      "cohort_ids": ["123", "456"],
      "is_noise": false
    }
  ],
  "metadata": {
    "total_results": 10,
    "exact_match_count": 847,
    "semantic_match_count": 234,
    "unique_patients": 187,
    "unique_encounters": 423,
    "unique_notes": 512,
    "query": "diabetes management",
    "search_type": "hybrid",
    "reranked": true,
    "distance_threshold": 0.7,
    "omitted_results": {
      "semantic_omitted": 89,
      "keyword_omitted": 67,
      "total_omitted": 156
    }
  }
}
```

#### Result Fields

| Field | Description |
|-------|-------------|
| `score` | Overall relevance score (higher = better) |
| `distance` | Cosine distance from query (lower = more similar, semantic only) |
| `keyword_score` | Normalized BM25 score (keyword/hybrid only) |
| `patient_id` | Patient identifier |
| `encounter_id` | Encounter identifier |
| `note_id` | Note identifier |
| `note_date` | Date of the note (YYYY-MM-DD) |
| `note_type` | Type of clinical note |
| `text_full` | Complete note text |
| `text_chunk` | Specific matching chunk |
| `cohort_ids` | Cohorts containing this note |
| `is_noise` | Whether note is flagged as noise |

---

### Noise Detection

The API automatically filters out "noise" notes (e.g., prescription lists, routine orders) by default. Control this behavior with:

- `include-noise=true` — Include all notes regardless of noise status
- `noise-categories-include` / `noise-categories-exclude` — Filter by noise category
- `noise-rules-include` / `noise-rules-exclude` — Filter by specific noise rules

#### List Noise Categories

```
GET /noise-categories
```

#### List Noise Rules

```
GET /noise-rules
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category-id` | string | — | Filter by category |
| `include-inactive` | boolean | false | Include inactive rules |

---

### Search History

#### List Search History

```
GET /search-history
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page-size` | integer | 20 | Items per page (1-100) |
| `user-id` | string | — | Filter by user |
| `search-type` | string | — | Filter by search type |
| `query` | string | — | Filter by query text |
| `date-from` | string | — | Filter from date |
| `date-to` | string | — | Filter to date |

#### Get Search Stats

```
GET /search-history/stats/summary
```

Returns aggregated metrics including total searches, unique queries, averages, and breakdowns by search type.

---

## Examples

### Python

```python
import requests

API_URL = "https://api.trioexplorer.example.com"
API_KEY = "ts_your_api_key_here"

# Search for diabetes-related notes
response = requests.get(
    f"{API_URL}/search",
    headers={"X-API-Key": API_KEY},
    params={
        "query": "diabetes management",
        "search-type": "hybrid",
        "k": 10,
        "cohort-ids": "123,456",
        "rerank": "true"
    }
)

results = response.json()
print(f"Found {len(results['results'])} results")

for result in results["results"]:
    print(f"Score: {result['score']:.4f} - {result['note_type']}")
```

### JavaScript

```javascript
const API_URL = "https://api.trioexplorer.example.com";
const API_KEY = "ts_your_api_key_here";

async function searchNotes(query, options = {}) {
  const params = new URLSearchParams({
    query,
    "search-type": options.searchType || "hybrid",
    k: options.k || 10,
    ...options
  });

  const response = await fetch(`${API_URL}/search?${params}`, {
    headers: { "X-API-Key": API_KEY }
  });

  return response.json();
}

// Usage
const results = await searchNotes("elevated blood pressure", {
  k: 20,
  "date-from": "2025-01-01"
});
```

### With Date Filters

```bash
curl -X GET "https://api.trioexplorer.example.com/search" \
  -H "X-API-Key: YOUR_API_KEY" \
  -G \
  --data-urlencode "query=heart failure" \
  --data-urlencode "k=20" \
  --data-urlencode "date-from=2025-01-01" \
  --data-urlencode "date-to=2025-06-30" \
  --data-urlencode "note-types=Progress Note,Discharge Summary"
```

### Comparing Search Types

```python
# Keyword search - best for exact terms
keyword_results = requests.get(
    f"{API_URL}/search",
    headers={"X-API-Key": API_KEY},
    params={"query": "ICD-10 E11.9", "search-type": "keyword", "k": 10}
).json()

# Semantic search - best for conceptual queries
semantic_results = requests.get(
    f"{API_URL}/search",
    headers={"X-API-Key": API_KEY},
    params={"query": "patient having trouble controlling blood sugar", "search-type": "semantic", "k": 10}
).json()

# Hybrid search - best of both worlds (default)
hybrid_results = requests.get(
    f"{API_URL}/search",
    headers={"X-API-Key": API_KEY},
    params={"query": "diabetes mellitus type 2", "search-type": "hybrid", "k": 10}
).json()
```

---

## Error Handling

| Status | Description |
|--------|-------------|
| `200` | Success |
| `400` | Invalid parameters (check error message for details) |
| `401` | Missing or invalid API key |
| `403` | Insufficient entitlements for requested scope |
| `404` | Resource not found (e.g., cohort not indexed) |
| `500` | Internal server error |

**Error Response Format:**

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Rate Limits & Performance

- **Response Time:** Sub-second for most queries
- **Reranking:** Adds 50-500ms depending on result count
- **Omitted Count:** Adds 50-200ms (use `skip-omitted-count=true` to skip)

For optimal performance:
- Use specific `cohort-ids` when possible
- Set `k` to only what you need
- Use `skip-omitted-count=true` for faster responses
- Consider `rerank=false` for exploratory searches

---

## Command-Line Interface

A CLI tool (`trioexplorer`) is available for interactive exploration and scripting.

### Installation

```bash
pip install ./cli
```

### Quick Start

```bash
# Set your API key
export TRIOEXPLORER_API_KEY="your_api_key_here"

# Search clinical notes
trioexplorer search "diabetes management"

# List available cohorts
trioexplorer list cohorts

# Get help
trioexplorer --help
```

See the [CLI documentation](cli/README.md) for full usage details.

---

## Support

For API access, issues, or feature requests, contact your administrator.

---

## License

Proprietary. All rights reserved.
