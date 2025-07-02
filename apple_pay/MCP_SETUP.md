# MCP Configuration Examples

## Using UV (Recommended)

### For Unix/Linux/macOS:
```json
{
  "mcpServers": {
    "apple_pay": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/apple_pay_mcp_server",
        "run",
        "apple_pay.py"
      ]
    }
  }
}
```

### For Windows:
```json
{
  "mcpServers": {
    "apple_pay": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/YourName/apple_pay_mcp_server",
        "run",
        "apple_pay.py"
      ]
    }
  }
}
```

## Using Python directly

### For Unix/Linux/macOS:
```json
{
  "mcpServers": {
    "apple_pay": {
      "command": "python",
      "args": ["/path/to/your/apple_pay_mcp_server/apple_pay.py"],
      "cwd": "/path/to/your/apple_pay_mcp_server"
    }
  }
}
```

### For Windows:
```json
{
  "mcpServers": {
    "apple_pay": {
      "command": "python",
      "args": ["C:/Users/YourName/apple_pay_mcp_server/apple_pay.py"],
      "cwd": "C:/Users/YourName/apple_pay_mcp_server"
    }
  }
}
```

## Setup Instructions

1. Choose the appropriate configuration for your OS
2. Replace the path with your actual installation directory
3. Add the configuration to your MCP client's config file
4. Restart your MCP client
