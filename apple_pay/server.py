#!/usr/bin/env python3
"""
Apple Pay MCP Server
Run this script to start the Apple Pay MCP server.
"""

if __name__ == "__main__":
    from apple_pay import mcp
    mcp.run(transport='stdio')
