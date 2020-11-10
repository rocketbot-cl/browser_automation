import websockets
import asyncio
import json


async def send_command_to_extension(instruction):
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        print("Sendig data to extension...")
        await websocket.send(instruction)
        extension_response = await websocket.recv()
        extension_response_json = json.loads(extension_response)
        if extension_response_json['status'] != 200:
            return
