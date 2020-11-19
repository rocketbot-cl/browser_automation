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
            extension_response = await websocket.recv()
            extension_response_json = json.loads(extension_response)
            if extension_response_json['status'] != 200:
                raise Exception(extension_response_json['status'])
            if result is not None:
                SetVar(result, extension_response_json['response'])
    except Exception as e:
        PrintException()
        raise e

if module == "click":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    click_type = GetParams("click_type")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "click"
        }
        instruction = json.dumps(instruction)
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
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction, result))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendkeys":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    special = GetParams("special")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "setValue",
            "data": special
        }
        instruction = json.dumps(instruction)
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendText":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    text = GetParams("text")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "setValue",
            "data": text
        }
        instruction = json.dumps(instruction)
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "openBrowser":
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

if module == "openUrl":
    import json
    url = GetParams("url")
    try:
        instruction = {
            "typeSelector": '',
            "selector": '',
            "command": "openUrl",
            "data": url
        }
        instruction = json.dumps(instruction)
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "waitObject":
    import json
    from time import sleep
    
    data_type = GetParams("data_type")
    data_selector = GetParams("data")
    waitBefore = GetParams("waitBefore")
    waitMax = GetParams("waitMax")
    waitAfter = GetParams("waitAfter")
    result = GetParams("result")
    
    try:
        data = {
            "waitMax": waitMax,
        }
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "waitObject",
            "data": data
        }
        instruction = json.dumps(instruction)
        if waitBefore:
            sleep(int(waitBefore))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction, result))
        if waitAfter:
            sleep(int(waitAfter))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getTable":
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
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction, result))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e