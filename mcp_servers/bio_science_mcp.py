"""Bio Science MCP Server — initial implementation.

Provides tools for querying PubMed, UniProt, and InterPro from Claude Code.

This server uses a minimal JSON-RPC 2.0 stdio loop to expose tools following
the Model Context Protocol (MCP) specification.

Run with: python -m mcp_servers.bio_science_mcp
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import traceback

from mcp_servers.adapters.interpro import search_interpro
from mcp_servers.adapters.pubmed import get_pubmed_abstract, search_pubmed
from mcp_servers.adapters.uniprot import get_uniprot_entry, search_uniprot

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("bio_science_mcp")


# ─── Tool Definitions ─────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "search_pubmed",
        "description": (
            "Search PubMed for articles matching a query. "
            "Returns pmid, title, authors, journal, and publication date."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (same syntax as PubMed web).",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Max articles to return (1-50).",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_pubmed_abstract",
        "description": (
            "Retrieve the full abstract of a PubMed article by its PMID."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "pmid": {
                    "type": "string",
                    "description": "PubMed ID (e.g. '35900023').",
                },
            },
            "required": ["pmid"],
        },
    },
    {
        "name": "search_uniprot",
        "description": (
            "Search UniProt for protein entries. "
            "Returns accession, protein name, gene, organism, review status."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Free-text or field query (e.g. 'insulin AND organism_name:human').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max entries to return (1-25).",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_uniprot_entry",
        "description": (
            "Get detailed UniProt entry by accession. Includes function, "
            "keywords, GO terms, sequence length."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "accession": {
                    "type": "string",
                    "description": "UniProt accession (e.g. 'P01308').",
                },
            },
            "required": ["accession"],
        },
    },
    {
        "name": "search_interpro",
        "description": (
            "Search InterPro for protein families, domains, and functional sites."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Text search (e.g. 'kinase', 'zinc finger').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max entries to return (1-20).",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
]


# ─── Tool Dispatch ────────────────────────────────────────────────────────────


async def _dispatch(tool_name: str, arguments: dict) -> str:
    """Route a tool call to the appropriate adapter function."""
    try:
        if tool_name == "search_pubmed":
            results = await search_pubmed(
                query=arguments["query"],
                max_results=arguments.get("max_results", 5),
            )
            return json.dumps([r.model_dump() for r in results], indent=2)

        elif tool_name == "get_pubmed_abstract":
            result = await get_pubmed_abstract(pmid=arguments["pmid"])
            return json.dumps(result.model_dump(), indent=2)

        elif tool_name == "search_uniprot":
            results = await search_uniprot(
                query=arguments["query"],
                limit=arguments.get("limit", 5),
            )
            return json.dumps([r.model_dump() for r in results], indent=2)

        elif tool_name == "get_uniprot_entry":
            result = await get_uniprot_entry(accession=arguments["accession"])
            return json.dumps(result.model_dump(), indent=2)

        elif tool_name == "search_interpro":
            results = await search_interpro(
                query=arguments["query"],
                limit=arguments.get("limit", 5),
            )
            return json.dumps([r.model_dump() for r in results], indent=2)

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    except Exception as exc:
        logger.error("Tool %s failed: %s", tool_name, traceback.format_exc())
        return json.dumps({"error": str(exc), "tool": tool_name})


# ─── MCP JSON-RPC Server Loop ─────────────────────────────────────────────────

SERVER_INFO = {
    "name": "bio-science-mcp",
    "version": "0.1.0",
    "description": "Bioinformatics MCP: PubMed, UniProt, InterPro",
}


async def _handle_request(request: dict) -> dict | None:
    """Handle a single JSON-RPC request."""
    method = request.get("method", "")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": SERVER_INFO,
                "capabilities": {"tools": {}},
            },
        }

    elif method == "notifications/initialized":
        # Client acknowledgement — no response needed
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        content = await _dispatch(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": content}],
            },
        }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    else:
        # Unknown method
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


def _write_response(response: dict) -> None:
    """Write a JSON-RPC response to stdout (thread-safe on Windows)."""
    out = json.dumps(response) + "\n"
    sys.stdout.buffer.write(out.encode())
    sys.stdout.buffer.flush()


def _read_line() -> bytes:
    """Read a single line from stdin (blocking)."""
    return sys.stdin.buffer.readline()


async def main() -> None:
    """Run the MCP server stdio loop (Windows-compatible)."""
    logger.info("bio-science-mcp starting (stdio)...")

    while True:
        line = await asyncio.to_thread(_read_line)
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received: %s", line[:100])
            continue

        response = await _handle_request(request)
        if response is not None:
            _write_response(response)

    logger.info("bio-science-mcp shutting down.")


if __name__ == "__main__":
    asyncio.run(main())
