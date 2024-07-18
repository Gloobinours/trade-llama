import asyncio
import websockets
import json

async def send_position(websocket, path):
    player_position = (1,2)
    while True:
        position_json = json.dumps(player_position)
    
        # Send position data to the client
        await websocket.send(position_json)

        # Wait before next update
        await asyncio.sleep(0.2)


# Define the function to handle incoming messages
async def server(websocket, path):
    # Continuously listen for incoming messages from the client
    async for message in websocket:
        print(f"Received message from client: {message}")
        # Example: Echo back the received message
        await websocket.send(message)

# Start WebSocket server
start_server = websockets.serve(server, '127.0.0.1', 5005)

# Run server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
