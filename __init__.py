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
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import websockets
import connection_server
from time import sleep
global browser_driver

module = GetParams("module")

types = {
        "name": By.NAME,
        "id": By.ID,
        "class name": By.CLASS_NAME,
        "xpath": By.XPATH,
        "tag name": By.TAG_NAME
    }


if module == "click":
    data_ = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    click_type = GetParams("click_type")
    wait_ = 5
    types = {
        "name": By.NAME,
        "id": By.ID,
        "class name": By.CLASS_NAME,
        "xpath": By.XPATH,
        "tag name": By.TAG_NAME
    }
    try:
        if not wait_:
            wait_ = 5
        actionChains = ActionChains(browser_driver)
        wait = WebDriverWait(browser_driver, int(wait_))
        try:
            elementLocator = wait.until(EC.element_to_be_clickable((types[data_type], data_)))
            browser_driver._object_selected = elementLocator
            actionChains.click(elementLocator).perform()
        except TimeoutException:
            raise Exception("The item is not available to be clicked")

    except Exception as e:
        print("\x1B[" + "31;40mEXCEPTION \x1B[" + "0m")
        PrintException()
        raise e

if module == "getText":
    import json 
    data_ = GetParams("data")
    data_type = GetParams("data_type")
    result = GetParams("result")
    wait_ = 5
    try:
        actionChains = ActionChains(browser_driver)
        wait = WebDriverWait(browser_driver, int(wait_))
        elementLocator = wait.until(EC.element_to_be_clickable((types[data_type], data_)))
        text_element = elementLocator.text
        SetVar(result, text_element)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e


if module == "sendText":
    import json 
    data_ = GetParams("data")
    data_type = GetParams("data_type")
    text = GetParams("text")
    wait_ = 5
    try:
        actionChains = ActionChains(browser_driver)
        wait = WebDriverWait(browser_driver, int(wait_))
        elementLocator = wait.until(EC.element_to_be_clickable((types[data_type], data_)))
        elementLocator.send_keys(text)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "openBrowser":
    import subprocess
    web = GetGlobals('web')
    web.driver_list[web.driver_actual_id] = browser_driver
    url = GetParams("url")
    path = GetParams("path")
    try:
        import subprocess

        platform_ = platform.system()
        subprocess.Popen(f"{path} --remote-debugging-port=5009")
        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:5009"
        if platform_.endswith('dows'):
            chrome_driver = os.path.join(base_path, os.path.normpath(r"drivers\win\chrome"), "chromedriver.exe")
        else:
            chrome_driver = os.path.join(base_path, os.path.normpath(r"drivers/mac/chrome"), "chromedriver")
        browser_driver = Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        web.driver_list[web.driver_actual_id] = browser_driver
        if url:
            browser_driver.get(url)

    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
