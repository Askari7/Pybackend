import asyncio
import websockets
import json

async def send_data(uri):
    async with websockets.connect(uri) as websocket:
        # Create the data you want to send
        data = {
            "In": 5,
            "Out": 3,
            "Time": "2024-09-30 10:00:00"
        }

        # Send the data as a JSON string
        await websocket.send(json.dumps(data))
        print(f"Sent data: {data}")

        # Wait for a response
        response = await websocket.recv()
        print(f"Received response: {response}")

# Define the WebSocket URI (adjust the port and IP address as needed)
websocket_uri = "ws://192.168.100.156:8080/ws/api/get-data/"

# Use asyncio.run() to execute the send_data coroutine
asyncio.run(send_data(websocket_uri))
