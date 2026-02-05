# Explorer Search API - Claude Code Guide

This repo is commonly used with Claude Code to search clinical notes. Here are quick tips to get started.

## Setup

1. **API Key**: Set up your API key in the system-wide config (recommended):
   ```bash
   mkdir -p ~/.trioexplorer
   echo "TRIOEXPLORER_API_KEY=ts_your_api_key_here" > ~/.trioexplorer/.env
   ```

   The CLI checks for the API key in this order:
   1. `~/.trioexplorer/.env` (system-wide, recommended)
   2. `.env` in the current directory or repo root
   3. `TRIOEXPLORER_API_KEY` environment variable

2. **Install the CLI** (for quick testing):
   ```bash
   pip install -e cli/
   ```

## Quick Testing with trioexplorer CLI

The `trioexplorer` CLI is the fastest way to test searches:

```bash
# Basic search (API key auto-loaded from ~/.trioexplorer/.env)
trioexplorer search "diabetes management"

# Limit results
trioexplorer search "chest pain" -k 5

# Semantic search
trioexplorer search "patient struggling with blood sugar" -t semantic

# List available cohorts
trioexplorer list cohorts
```

## Common Search Parameters

- `query`: Your search text (required)
- `-k`: Number of results (default: 10, max: 10,000)
- `-t` / `--search-type`: `hybrid`, `semantic`, or `keyword`
- `--cohort-ids`: Filter by cohort IDs (comma-separated)
- `--patient-id`: Filter to a specific patient UUID
- `--distinct`: De-duplication mode (`encounter`, `patient`, `note`, `none`)

## Retrieving All Notes for a Patient

To get all notes for a specific patient, use keyword search with a common term (empty queries are not supported):

```bash
# Get all notes for a patient (up to 10k)
trioexplorer search "patient" --patient-id <UUID> -k 10000 -t keyword --rerank false --distinct note

# Alternative common terms that appear in most notes: "the", "and", "is"
```

**Note:** Results are ordered by relevance score, not by date. There is currently no sort option in the API.
