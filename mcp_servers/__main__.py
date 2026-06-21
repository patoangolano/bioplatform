"""Allow running as `python -m mcp_servers.bio_science_mcp`."""
from mcp_servers.bio_science_mcp import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
