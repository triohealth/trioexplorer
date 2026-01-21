# Explorer Search API

A hybrid search API for clinical notes, combining semantic vector search with BM25 keyword matching.

> **Note:** To get an API key, contact sales@trioehealth.com

## Documentation

- **[API Reference](https://triohealth.github.io/explorer-search-api/)** — Full OpenAPI documentation with interactive examples
- **[Getting Started Notebook](notebooks/getting_started.ipynb)** — Interactive tutorial with visualizations

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/triohealth/explorer-search-api/blob/main/notebooks/getting_started.ipynb)

## Quick Start

```bash
export TRIO_API_URL="http://k8s-notesear-notesear-20ee5f12c9-4c4972a75575c8a7.elb.us-east-1.amazonaws.com:8001"
export TRIO_API_KEY="YOUR_API_KEY"

# Search across all cohorts
curl -X GET "$TRIO_API_URL/search" \
  -H "X-API-Key: $TRIO_API_KEY" \
  -G \
  --data-urlencode "query=diabetes management" \
  --data-urlencode "k=10"

# List available cohorts
curl -X GET "$TRIO_API_URL/cohorts/indexed" \
  -H "X-API-Key: $TRIO_API_KEY"
```

## CLI

Install and use the command-line interface for interactive exploration:

```bash
pip install ./cli

export TRIOEXPLORER_API_KEY="your_api_key_here"

trioexplorer search "diabetes management"
trioexplorer list cohorts
trioexplorer --help
```

See [cli/README.md](cli/README.md) for full documentation.

## Support

For API access, issues, or feature requests, contact sales@triohealth.com

## License

Proprietary. All rights reserved.
