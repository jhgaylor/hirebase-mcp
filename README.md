# Simple MCP Server

A simple Mission Control Protocol (MCP) server implementation using FastAPI and WebSockets.

## Features

- WebSocket-based communication
- Client connection management
- JSON message handling
- Basic error handling and logging
- REST endpoints for server status and client information
- Modern Python packaging with `uv`

## Project Structure

```
.
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── __main__.py
│       └── server.py
├── pyproject.toml
└── README.md
```

## Setup

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a new virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -e .
```

## Running the Server

Start the server with:
```bash
python -m mcp_server
```

The server will run on `http://localhost:8000` with the following endpoints:

- `GET /` - Server status check
- `GET /clients` - List connected clients
- `WebSocket /ws/{client_id}` - WebSocket connection endpoint

## WebSocket Usage Example

You can test the WebSocket connection using a Python client like this:

```python
import websockets
import asyncio
import json

async def test_connection():
    uri = "ws://localhost:8000/ws/test-client"
    async with websockets.connect(uri) as websocket:
        # Send a test message
        message = {"type": "test", "content": "Hello, MCP Server!"}
        await websocket.send(json.dumps(message))
        
        # Receive the response
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(test_connection())
```

## Development

This project uses:
- `uv` for dependency management and virtual environments
- `ruff` for linting and formatting
- `hatch` as the build backend

### Common Tasks

```bash
# Update dependencies
uv pip compile pyproject.toml -o requirements.txt

# Run linting
ruff check .

# Format code
ruff format .
```

## API Documentation

Once the server is running, you can access the automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 