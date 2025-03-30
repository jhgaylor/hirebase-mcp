from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple MCP Server")

# Store active connections
connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connections[client_id] = websocket
    logger.info(f"Client {client_id} connected")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                logger.info(f"Received message from {client_id}: {message}")
                
                # Echo the message back to the client
                response = {
                    "status": "success",
                    "message": "Message received",
                    "data": message
                }
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_id}")
                await websocket.send_json({
                    "status": "error",
                    "message": "Invalid JSON format"
                })
                
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected")
        connections.pop(client_id, None)
    except Exception as e:
        logger.error(f"Error handling message from {client_id}: {str(e)}")
        connections.pop(client_id, None)

@app.get("/")
async def root():
    return {"message": "MCP Server is running", "status": "ok"}

@app.get("/clients")
async def get_clients():
    return {"connected_clients": list(connections.keys())} 