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
from selenium.webdriver import Chrome # type: ignore
from selenium.webdriver import ActionChains # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import platform
import socket
import subprocess
import psutil

BASE_PATH = tmp_global_obj["basepath"] # type: ignore
cur_path = BASE_PATH + 'modules' + os.sep + 'browser_automation' + os.sep + 'libs' + os.sep
uc_path = BASE_PATH + 'modules' + os.sep + 'browser_automation' + os.sep + 'libs' + os.sep + 'src' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)
if uc_path not in sys.path:
    sys.path.append(uc_path)


systems = {
    'Linux': "linux", 
    'Darwin': "mac",
    'Windows': "win"
}
SYSTEM = platform.system()

GetGlobals = GetGlobals # type: ignore
GetParams = GetParams # type: ignore
SetVar = SetVar # type: ignore
PrintException = PrintException # type: ignore

session = GetParams("session")
if not session:
    session = 'default'

web = GetGlobals('web')

module = GetParams("module")
global terminate_chromedriver, _is_port_free, _find_free_port, _to_bool
def terminate_chromedriver(port):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'chromedriver.exe' and f'--port={port}' in proc.info['cmdline']:
            proc.kill()
            break


def _is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as port_socket:
        return port_socket.connect_ex(('127.0.0.1', int(port))) != 0


def _find_free_port(start_port=5002, end_port=5100):
    for candidate_port in range(start_port, end_port + 1):
        if _is_port_free(candidate_port):
            return str(candidate_port)
    raise RuntimeError("No free debugging port available for browser automation")


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("true", "1", "yes", "on")

class BrowserAutomation:
    global BASE_PATH, systems, SYSTEM, socket
    
    DRIVERS = {
        "chrome": "chromedriver",
        "firefox": "x64" + os.sep + "geckodriver"
    }
   
    def __init__(self, browser="chrome", driver_path=None, browser_path="", folderPath="", port="5002", search=False, download_dir=None, session_name="default"):
        self.driver = None
        self.driver_path = driver_path
        self.browser = browser
        self.browser_path = browser_path
        self.port = str(port)
        self.download_dir = download_dir
        self.session_name = session_name or "default"
        
        if _to_bool(search):
            self.port = _find_free_port()
        elif not _is_port_free(self.port):
            self.port = _find_free_port(start_port=int(self.port) + 1)
        
        if folderPath and folderPath.strip() and folderPath != " ":
            self.profile_path = folderPath if " " not in folderPath else "\"" + folderPath + "\""
        else:
            folderPath = os.path.join(BASE_PATH, 'modules', 'browser_automation', 'profile', self.session_name)
            self.profile_path = folderPath if " " not in folderPath else "\"" + folderPath + "\""
    
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

    def launch_browser(self, force_renderer=False):
        import subprocess
        if force_renderer:
            print("for renderer")
            subprocess.Popen(" ".join([self.browser_path, "--force-renderer-accessibility --kiosk-printing --remote-debugging-port="+self.port, "--user-data-dir=" + self.profile_path + ""]), shell=True)
        else:
            subprocess.Popen(" ".join([self.browser_path, "--kiosk-printing --remote-debugging-port="+self.port, "--user-data-dir=" + self.profile_path + ""]), shell=True)
    
    def open(self, force_renderer=False):
        global Options, Chrome
        self.launch_browser(force_renderer=force_renderer)
        if self.browser == "chrome":
            chrome_options = Options()
            chrome_options.debugger_address = "127.0.0.1:" + self.port
            self.driver = Chrome(chrome_options=chrome_options, executable_path=self.driver_path)
            self.set_download_dir()
            return self.driver
    
    def open_undetected(self, force_renderer=False):
        global Options, Chrome
        self.launch_browser()
        if self.browser == "chrome":
            import r_undetected_chromedriver as uc # type: ignore
            print(uc.__file__)
            # uc.install(
            #     executable_path = self.driver_path ,
            # )
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            if force_renderer:
                options.add_argument('--force-renderer-accessibility')
            # options.add_argument('--headless')
            # options.add_argument('--enable-javascript')
            # options.add_argument('--disable-gpu')
            # options.experimental_options["debuggerAddress"] = "127.0.0.1:" + self.port
            options.debugger_address = "127.0.0.1:" + self.port
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
            options.add_argument('User-Agent={0}'.format(user_agent))
            options.user_data_dir = self.profile_path
            print(self.driver_path)
            self.driver = uc.Chrome(options=options, browser_executable_path=self.driver_path, executable_path=self.driver_path)
            print("opening")
            self.set_download_dir()
            # chrome_options = Options()
            # chrome_options.debugger_address = "127.0.0.1:" + self.port
            # self.driver = Chrome(chrome_options=chrome_options, executable_path=self.driver_path)
            return self.driver
    def set_download_dir(self):
        """Configura la carpeta de descargas mediante CDP (funciona también en headless).
        Se llama automáticamente desde open() / open_undetected()."""
        if not self.download_dir or not self.driver:
            return
        import os
        d = os.path.abspath(self.download_dir)
        
        os.makedirs(d, exist_ok=True)

        if SYSTEM == "Windows":
            d = d.replace("/", "\\")
        try:
            self.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": d
            })
        except Exception as e:
            
            try:
                self.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                    "behavior": "allowAndName",
                    "downloadPath": d,
                    "eventsEnabled": True
                })
            except Exception:
                print("Could not pin download folder via CDP:", repr(e))

if module == "openBrowser":

    url = GetParams("url")
    path = GetParams("path")
    browser = GetParams("browser")
    folder = GetParams("folder")
    port = GetParams("port")
    search_port = GetParams("search_port")
    force_renderer = eval(GetParams("force_renderer_accessibility")) if GetParams("force_renderer_accessibility") else False
    download_dir=GetParams("downloads_folder")
    session = GetParams("session")

    if folder == None or folder == "":
        folder = " "

    if port == None or port == "":
        port = "5002"
        
    if search_port == None or search_port == "":
        search_port = False
    
    try:
        browser_ = "chrome"
        if session in web.driver_list:
            try:
                web.driver_list[session].quit()
            except Exception:
                pass
            finally:
                web.driver_list.pop(session, None)

        browser_automation = BrowserAutomation(
            browser_,
            browser_path=path,
            folderPath=folder,
            port=port,
            search=search_port,
            download_dir=download_dir,
            session_name=session
        )
        
        if browser == 'undetected_chrome':
            browser_driver = browser_automation.open_undetected(force_renderer=force_renderer)
        else:
            browser_driver = browser_automation.open(force_renderer=force_renderer)

        web.driver_list[session] = browser_driver
        web.driver_actual_id = session
        if url:
            browser_driver.get(url)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "closeBrowser":
    try:
        session = GetParams("session")
        browser_driver = web.driver_list[session]
        mod_chromedriver_port = browser_driver.service.port
        browser_driver.close()
        browser_driver.quit()
        web.driver_list.pop(session, None)

    except Exception as e:
        try:
            terminate_chromedriver(mod_chromedriver_port)
            if session in web.driver_list:
                web.driver_list[session].quit()
                web.driver_list.pop(session, None)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e

