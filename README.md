# Bio Science MCP Server

MCP server for bioinformatics queries — PubMed, UniProt, and InterPro integration for Claude Code.

## Status

**v0.1.0 — Initial implementation.** This is a functional MCP server using a minimal JSON-RPC 2.0 stdio transport. It does not depend on an external MCP SDK; the protocol loop is self-contained.

## Tools Available

| Tool | Description |
|------|-------------|
| `search_pubmed` | Search PubMed articles by query |
| `get_pubmed_abstract` | Get full abstract by PMID |
| `search_uniprot` | Search UniProt protein entries |
| `get_uniprot_entry` | Get detailed protein entry by accession |
| `search_interpro` | Search InterPro families/domains |

## Installation (Windows PowerShell)

```powershell
# From the bioplatform root directory:
cd C:\Users\Manec\bioplatform

# Create virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements-mcp.txt
```

## Running Manually (for testing)

```powershell
python -m mcp_servers.bio_science_mcp
```

The server reads JSON-RPC messages from stdin and writes responses to stdout. It's designed to be launched by Claude Code, not used interactively.

## Registering in Claude Code

The `.mcp.json` in this repository already includes the `scientific-bio` entry. If you need to add it manually:

```json
{
  "mcpServers": {
    "scientific-bio": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_servers.bio_science_mcp"]
    }
  }
}
```

## Environment Variables (optional)

| Variable | Purpose |
|----------|---------|
| `NCBI_API_KEY` | Increases PubMed rate limit from 3 to 10 req/s |

## Project Structure

```
mcp_servers/
  __init__.py
  __main__.py            # Entry point for python -m
  bio_science_mcp.py     # MCP server loop + tool registry
  models.py              # Pydantic response models
  adapters/
    __init__.py
    pubmed.py            # NCBI E-utilities adapter
    uniprot.py           # UniProt REST API adapter
    interpro.py          # InterPro API adapter
```

## Limitations

- No streaming; responses are returned in full.
- InterPro search is full-text only (no boolean operators).
- PubMed XML parsing uses `defusedxml` for security.
- No caching layer yet — every call hits the upstream API.
- Rate limiting relies on upstream API defaults (no client-side throttle).

## Next Steps

- Add BLAST sequence search adapter
- Add caching (Redis or local TTL cache)
- Add PDB/AlphaFold structure lookup
- Integrate with the `postgres` MCP for local provenance storage
- Add proper MCP SDK once a stable Python SDK is adopted