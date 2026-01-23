# Explorer Search API - Claude Code Guide

This repo is commonly used with Claude Code to search clinical notes. Here are quick tips to get started.

## Setup

1. **API Key**: Check for your API key in the `.env` file at the repo root:
   ```
   TRIOEXPLORER_API_KEY=ts_your_api_key_here
   ```

2. **Install the CLI** (for quick testing):
   ```bash
   pip install -e cli/
   ```

## Quick Testing with trioexplorer CLI

The `trioexplorer` CLI is the fastest way to test searches:

```bash
# Load your API key
export $(cat .env | xargs)

# Basic search
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
- `-k`: Number of results (default: 10)
- `-t` / `--search-type`: `hybrid`, `semantic`, or `keyword`
- `--cohort-ids`: Filter by cohort IDs (comma-separated)
