# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
   sudo pip install <package> -t .

"""

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'browser_automation' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)

import websockets
import connection_server
from time import sleep
global websockets

module = GetParams("module")


async def send_command_to_extension(instruction, result=None):
    import json
    try:
        uri = "ws://localhost:8000"
        async with websockets.connect(uri) as websocket:
            print("Sendig data to extension...")
            await websocket.send(instruction)
            print("Instruction: " + str(instruction))
            extension_response = await websocket.recv()
            print(type(extension_response))
            extension_response_json = json.loads(extension_response)
            print("Respuesta: ", type(extension_response_json))
            if extension_response_json['status'] != 200:
                raise Exception(extension_response_json['status'])
            if result is not None:
                SetVar(result, extension_response_json['response'])
    except Exception as e:
        #print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "click":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    print("******************************************* \n \n")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "click"
        }
        instruction = json.dumps(instruction)
        print("La instruccion es la siguiente: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        
        raise e

if module == "getText":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "getValue"
        }
        instruction = json.dumps(instruction)
        print("La instruccion es la siguiente: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction, result))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendkeys":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    text = GetParams("text")
    special = GetParams("special")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "setValue"
        }
        if text or special:
            instruction["data"] = text if text else special

            instruction = json.dumps(instruction)
            print("La instruccion es la siguiente: " + str(instruction))
            connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendText":
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    wait_seconds = GetParams("wait")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "setValue"
        }
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "openUrl":
    import subprocess
    url = GetParams("url")
    path = GetParams("path")
    try:
        subprocess.Popen(f"{path} {url}")
        sleep(10)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
