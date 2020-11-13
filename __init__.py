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
global websockets

module = GetParams("module")


async def send_command_to_extension(instruction):
    try:
        uri = "ws://localhost:8000"
        async with websockets.connect(uri) as websocket:
            print("Sendig data to extension...")
            await websocket.send(instruction)
            print("Instruction: " + str(instruction))
            extension_response = await websocket.recv()
            extension_response_json = json.loads(extension_response)
            print("Respuesta: " + str(extension_response_json))
            #if extension_response_json['status'] != 200:
            #    return
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        #PrintException()
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
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e

if module == "getText":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    print("******************************************* \n \n")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "getValue"
        }
        instruction = json.dumps(instruction)
        print("La instruccion es la siguiente: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendkeys":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    print("******************************************* \n \n")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "getValue"
        }
        instruction = json.dumps(instruction)
        print("La instruccion es la siguiente: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
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
            "command": "click"
        }
        connection_server.asyncio.get_event_loop().run_until_complete(connection_server.send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e