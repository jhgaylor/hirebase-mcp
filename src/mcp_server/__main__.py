import uvicorn
from mcp_server.server import app

def main():
    """Run the MCP server."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 