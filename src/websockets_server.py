import asyncio
import websockets
import json
from Maze import Maze

maze: Maze = Maze(60, 3)

async def send_maze_data(websocket, path):
    mtx = []
    for x in range(maze.size):
        mtx.append([])
        for y in range(maze.size):
            mtx[x].append(maze.maze_mtx[x][y].state.value)

    while True:
        try:
            mtx_json = json.dumps(mtx)
        
            # Send maze data to the client
            await websocket.send(mtx_json)

            # Wait before next update
            await asyncio.sleep(1)
        except Exception as e:
            print(f'Error sending maze data: {e}')


# Handle incoming messages
async def server(websocket, path):

    asyncio.create_task(send_maze_data(websocket, path))
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
