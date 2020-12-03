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

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import websockets
import connection_server
from time import sleep
global browser_driver

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

if module == "connect":

    server_app = base_path + 'modules/browser_automation/bin/server.exe'
    script_path = base_path + 'modules/browser_automation/libs/script.js'
    instruction = {
        "data": script_path
    }
    connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))


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
        import subprocess

        platform_ = platform.system()
        subprocess.Popen(f"{path} --remote-debugging-port=5004")
        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:5004"
        if platform_.endswith('dows'):
            chrome_driver = os.path.join(base_path, os.path.normpath(r"drivers\win\chrome"), "chromedriver.exe")
        else:
            chrome_driver = os.path.join(base_path, os.path.normpath(r"drivers/mac/chrome"), "chromedriver")
        browser_driver = Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        if url:
            browser_driver.get(url)

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
            "command": "getTable"
        }
        instruction = json.dumps(instruction)
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction, result))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "takeScreenshot":
    import json 
    data_selector = GetParams("data")
    data_type = GetParams("data_type")
    name = GetParams("name")
    try:
        instruction = {
            "typeSelector": data_type,
            "selector": data_selector,
            "command": "takeScreenshot",
            "data": name
        }
        instruction = json.dumps(instruction)
        print("La instruccion es: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "executeJs":
    import json 
    script = GetParams("cualquiercosa")
    script_path = GetParams("script_path")
    if script and script_path:
        raise Exception("No puede elegir ambos campos, seleccione uno solo.")
    try:
        instruction = {
                "typeSelector": '',
                "selector": '',
                "command": "executeJs"
            }
        if script is not None:
            instruction["data"] = script
        if script_path is not None:
            script_file = open(script_path)
            script_content = script_file.read()
            print(script_content)
            instruction["data"] = script_content
        instruction = json.dumps(instruction)
        print("La instruccion es: " + str(instruction))
        connection_server.asyncio.get_event_loop().run_until_complete(send_command_to_extension(instruction))
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
