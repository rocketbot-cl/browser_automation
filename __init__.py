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

import sys
import os
from selenium.webdriver import Chrome
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import platform

BASE_PATH = tmp_global_obj["basepath"] # Rocketbot path
cur_path = BASE_PATH + 'modules' + os.sep + 'browser_automation' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)


systems = {
    'Linux': "linux", 
    'Darwin': "mac",
    'Windows': "win"
}
SYSTEM = platform.system()

web = GetGlobals('web')
module = GetParams("module")
class BrowserAutomation:
    global BASE_PATH, systems, SYSTEM


    DRIVERS = {
        "chrome": "chromedriver",
        "firefox": "x64" + os.sep + "geckodriver"
    }
   
    def __init__(self, browser="chrome", driver_path=None, browser_path=""):
        self.driver_path = driver_path
        self.browser = browser
        self.browser_path = browser_path
        self.port = "5005"
        self.profile_path = os.path.join(BASE_PATH,'modules','browser_automation','profile').replace(" ", "' '")

    @property
    def driver_path(self):
        if self.__driver_path:
            return self.__driver_path

        driver_name = self.DRIVERS[self.browser] + (".exe" if SYSTEM == "Windows" else "")
        return os.path.join(BASE_PATH, "drivers", systems[SYSTEM], self.browser, driver_name)

    @driver_path.setter
    def driver_path(self, path):
        self.__driver_path = path

    @property
    def browser_path(self):
        BROWSER_PATHS = {
            "chrome": {
                "Windows": 'start "" chrome',
                "Linux": "/usr/bin/google-chrome",
                "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            }
        }

        if self.__browser_path:
            return self.__browser_path
        return BROWSER_PATHS[self.browser][SYSTEM]

    @browser_path.setter
    def browser_path(self, path):
        self.__browser_path = path

    def launch_browser(self):
        import subprocess
        subprocess.Popen(" ".join([self.browser_path, "--remote-debugging-port="+self.port, "--user-data-dir=" + self.profile_path]), shell=True)
    
    def open(self):
        global Options, Chrome
        self.launch_browser()
        if self.browser == "chrome":
            chrome_options = Options()
            chrome_options.debugger_address = "127.0.0.1:" + self.port
            self.driver = Chrome(chrome_options=chrome_options, executable_path=self.driver_path)
            return self.driver


if module == "openBrowser":

    url = GetParams("url")
    path = GetParams("path")
    browser = GetParams("browser")

    try:
        if path:
            browser = "chrome"

        browser_automation = BrowserAutomation(browser, browser_path=path)
        browser_driver = browser_automation.open()

        web.driver_list[web.driver_actual_id] = browser_driver
        if url:
            browser_driver.get(url)

    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "closeBrowser":
    browser_driver = web.driver_list[web.driver_actual_id]
    browser_driver.close()
    browser_driver.quit()
