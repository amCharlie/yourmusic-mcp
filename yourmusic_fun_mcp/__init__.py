"""YourMusic.Fun MCP Server package."""
from .api import mcp


def main():
    """MCP YourMusic.Fun api Server - HTTP call YourMusic.Fun API for MCP"""
    mcp.run()


if __name__ == "__main__":
    main()
