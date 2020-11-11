import websockets
import asyncio
import json


async def send_command_to_extension(instruction):
    try:
        uri = "ws://localhost:8000"
        async with websockets.connect(uri) as websocket:
            print("Sendig data to extension...")
            await websocket.send(instruction)
            print("Instruction: " + str(instruction))
            extension_response = await websocket.recv()
            extension_response_json = json.loads(extension_response)
            if extension_response_json['status'] != 200:
                return
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e