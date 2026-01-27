# Trioexplorer CLI

Command-line interface for the Trioexplorer API with full feature coverage.

## Installation

```bash
cd cli
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Configuration

Store your API key in the system-wide config (recommended):

```bash
mkdir -p ~/.trioexplorer
echo "TRIOEXPLORER_API_KEY=ts_your_api_key_here" > ~/.trioexplorer/.env
```

The CLI looks for the API key in this order:

1. `~/.trioexplorer/.env` (system-wide, recommended)
2. `.env` in the current directory or repo root
3. `TRIOEXPLORER_API_KEY` environment variable

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRIOEXPLORER_API_KEY` | Yes | | API key with read entitlements |
| `TRIOEXPLORER_API_URL` | No | Production ELB | Search API base URL |

To get an API key, contact sales@trioehealth.com

## Usage

### Search

```bash
# Basic search
trioexplorer search "chest pain"

# With result count and search type
trioexplorer search "chest pain" -k 20 --type semantic

# Cohort filtering
trioexplorer search "diabetes" --cohort-ids abc123,def456

# Patient/encounter filtering
trioexplorer search "medication history" --patient-id "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"
trioexplorer search "vital signs" --encounter-id "ABC12345-6789-0DEF-GHIJ"

# Note type and date filtering
trioexplorer search "discharge planning" --note-types "Discharge Summary,Progress Note"
trioexplorer search "recent visits" --date-from 2025-01-01 --date-to 2025-06-30

# Quality filtering
trioexplorer search "cardiac" --min-quality-score 0.8 --min-chunk-quality-score 0.7

# Advanced tuning
trioexplorer search "pneumonia" \
  --rerank false \
  --vector-weight 0.5 \
  --distance-threshold 0.6 \
  --chunk-multiplier 3.0 \
  --top-k-retrieval 500

# Custom metadata filters
trioexplorer search "sepsis" --filters '[["note_type", "Eq", "DISCHARGE SUMMARY"]]'

# Entity filters (medications, labs, vitals, diagnoses, etc.)
trioexplorer search "diabetes" --entity-filters '{"medications_present": ["metformin"]}'
trioexplorer search "kidney function" --entity-filters '{"lab_tests": ["creatinine", "GFR"]}'
trioexplorer search "hypertension" --entity-filters '{"vitals": ["blood pressure", "BP"]}'

# See FILTERS.md for comprehensive filter documentation

# Output formats
trioexplorer search "coughing" --format json
trioexplorer search "coughing" --format csv
trioexplorer search "coughing" --format table  # default

# Full text output
trioexplorer search "coughing" --full-text
```

### List Resources

```bash
# List indexed cohorts
trioexplorer list cohorts
trioexplorer list cohorts --limit 50

# List note types
trioexplorer list notetypes
trioexplorer list notetypes --search "discharge"
trioexplorer list notetypes --limit 100

# List search history
trioexplorer list history
trioexplorer list history --page 2 --page-size 50
trioexplorer list history --user-id user@example.com
trioexplorer list history --type semantic
trioexplorer list history --query "diabetes"
trioexplorer list history --date-from 2025-01-01 --date-to 2025-01-31

# List entity types for filtering
trioexplorer list entities

# List filter fields
trioexplorer list filters
trioexplorer list filters --field note_type
```

### Get Resources by ID

```bash
# Get specific history entry
trioexplorer get history <history_id>
```

### Statistics

```bash
# Get search stats summary
trioexplorer stats history
trioexplorer stats history --date-from 2025-01-01 --date-to 2025-01-31
```

## Global Options

| Flag | Description |
|------|-------------|
| `--debug` | Enable request/response logging |
| `--api-url URL` | Override TRIOEXPLORER_API_URL |
| `--version` | Print version |
| `--help` | Show help |

## Output Formats

### Table (default)
Rich-formatted tables with:
- Truncated text columns
- Color-coded scores
- Pagination info in footer

### JSON
Raw API response for scripting/piping:
```bash
trioexplorer search "query" --format json | jq '.results[0]'
```

### CSV
Export-friendly format:
```bash
trioexplorer search "query" --format csv > results.csv
```

## Development

### Running Tests

```bash
cd cli
pip install -e ".[dev]"
pytest
```

### Project Structure

```
cli/
├── README.md
├── pyproject.toml
├── requirements.txt
├── trioexplorer/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── client.py        # HTTP client
│   ├── auth.py          # API key handling
│   ├── config.py        # Configuration
│   ├── output.py        # Formatters
│   └── commands/
│       ├── search.py    # Search command
│       ├── list.py      # List commands
│       ├── history.py   # History commands
│       └── stats.py     # Stats commands
└── tests/
    ├── conftest.py
    ├── test_search.py
    ├── test_list.py
    ├── test_history.py
    └── test_output.py
```
