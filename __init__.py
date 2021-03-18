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
from time import sleep
global browser_driver

module = GetParams("module")


if module == "openBrowser":
    import subprocess
    web = GetGlobals('web')

    url = GetParams("url")
    path = GetParams("path")
    try:
        import subprocess

        platform_ = platform.system()
        profile = base_path + 'modules' + os.sep + 'browser_automation' + os.sep + 'profile' + os.sep
        res = subprocess.Popen(f"{path} --remote-debugging-port=5005 --user-data-dir={profile}")
        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:5005"
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

if module == "closeBrowser":
    browser_driver.close()
    browser_driver.quit()
