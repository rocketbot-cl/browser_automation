import os
import runpy
import subprocess
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "__init__.py"


class BrowserDriver:
    def __init__(self, service=None, browser_process=None):
        if service is not None:
            self.service = service
        if browser_process is not None:
            self._rocketbot_browser_process = browser_process
        self.close = Mock()
        self.quit = Mock()


def runtime_modules():
    selenium = types.ModuleType("selenium")
    selenium.__path__ = []
    webdriver = types.ModuleType("selenium.webdriver")
    webdriver.__path__ = []
    webdriver.Chrome = Mock()
    webdriver.ActionChains = Mock()
    chrome = types.ModuleType("selenium.webdriver.chrome")
    chrome.__path__ = []
    options = types.ModuleType("selenium.webdriver.chrome.options")
    options.Options = Mock()
    selenium.webdriver = webdriver
    webdriver.chrome = chrome
    chrome.options = options

    psutil = types.ModuleType("psutil")
    psutil.NoSuchProcess = type("NoSuchProcess", (Exception,), {})
    psutil.AccessDenied = type("AccessDenied", (Exception,), {})
    psutil.ZombieProcess = type("ZombieProcess", (Exception,), {})
    psutil.process_iter = Mock(return_value=[])

    return {
        "selenium": selenium,
        "selenium.webdriver": webdriver,
        "selenium.webdriver.chrome": chrome,
        "selenium.webdriver.chrome.options": options,
        "psutil": psutil,
    }, psutil


class BrowserAutomationCloseTests(unittest.TestCase):
    def run_close(self, driver_list, session=None, system="Linux", processes=None):
        modules, psutil = runtime_modules()
        psutil.process_iter.return_value = processes or []
        params = {"module": "closeBrowser", "session": session}
        web = SimpleNamespace(driver_list=driver_list)
        globals_ = {
            "tmp_global_obj": {"basepath": str(PROJECT_ROOT) + os.sep},
            "GetParams": lambda name: params.get(name),
            "GetGlobals": lambda name: web,
            "SetVar": Mock(),
            "PrintException": Mock(),
        }
        with patch.dict(sys.modules, modules), patch(
            "platform.system", return_value=system
        ), patch.object(sys, "path", sys.path.copy()):
            namespace = runpy.run_path(str(MODULE_PATH), init_globals=globals_)
        return namespace, psutil

    def test_default_session_is_closed(self):
        driver = BrowserDriver()
        driver_list = {"default": driver}

        self.run_close(driver_list)

        driver.close.assert_called_once_with()
        driver.quit.assert_called_once_with()
        self.assertNotIn("default", driver_list)

    def test_explicit_session_is_closed(self):
        driver = BrowserDriver()
        driver_list = {"checkout": driver}

        self.run_close(driver_list, session="checkout")

        driver.close.assert_called_once_with()
        driver.quit.assert_called_once_with()
        self.assertNotIn("checkout", driver_list)

    def test_missing_session_is_a_no_op(self):
        driver_list = {}

        self.run_close(driver_list, session="missing")

        self.assertEqual(driver_list, {})

    def test_windows_quit_failure_kills_driver_by_available_service_port(self):
        driver = BrowserDriver(service=SimpleNamespace(port=9515))
        driver.quit.side_effect = [RuntimeError("quit failed"), RuntimeError("retry failed")]
        driver_list = {"default": driver}
        process = SimpleNamespace(
            info={"name": "chromedriver", "cmdline": ["chromedriver", "--port=9515"]},
            kill=Mock(),
        )

        _, psutil = self.run_close(driver_list, system="Windows", processes=[process])

        driver.quit.assert_has_calls([call(), call()])
        psutil.process_iter.assert_called_once_with(["pid", "name", "cmdline"])
        process.kill.assert_called_once_with()
        self.assertNotIn("default", driver_list)

    def test_windows_quit_failure_without_service_retries_without_terminating(self):
        driver = BrowserDriver()
        driver.quit.side_effect = [RuntimeError("quit failed"), RuntimeError("retry failed")]
        driver_list = {"default": driver}

        _, psutil = self.run_close(driver_list, system="Windows")

        self.assertEqual(driver.quit.call_count, 2)
        psutil.process_iter.assert_not_called()
        self.assertNotIn("default", driver_list)

    def test_normal_windows_close_does_not_terminate_processes(self):
        driver = BrowserDriver(service=SimpleNamespace(port=9515))
        driver_list = {"default": driver}

        _, psutil = self.run_close(driver_list, system="Windows")

        driver.close.assert_called_once_with()
        driver.quit.assert_called_once_with()
        psutil.process_iter.assert_not_called()

    def test_macos_terminates_remaining_browser_process_without_close(self):
        process = Mock()
        process.poll.return_value = None
        process.wait.return_value = 0
        driver = BrowserDriver(browser_process=process)
        driver_list = {"default": driver}

        self.run_close(driver_list, system="Darwin")

        driver.close.assert_not_called()
        driver.quit.assert_called_once_with()
        process.terminate.assert_called_once_with()
        process.wait.assert_called_once_with(timeout=5)
        process.kill.assert_not_called()
        self.assertNotIn("default", driver_list)

    def test_macos_kills_browser_process_after_terminate_timeout(self):
        process = Mock()
        process.poll.return_value = None
        process.wait.side_effect = [
            subprocess.TimeoutExpired(cmd="chrome", timeout=5),
            0,
        ]
        driver = BrowserDriver(browser_process=process)
        driver_list = {"default": driver}

        self.run_close(driver_list, system="Darwin")

        driver.close.assert_not_called()
        process.terminate.assert_called_once_with()
        process.wait.assert_has_calls(
            [call(timeout=5), call(timeout=5)]
        )
        process.kill.assert_called_once_with()
        self.assertNotIn("default", driver_list)

    def test_driver_dictionary_is_cleaned_even_if_macos_process_cleanup_fails(self):
        process = Mock()
        process.poll.return_value = None
        process.terminate.side_effect = RuntimeError("terminate failed")
        driver = BrowserDriver(browser_process=process)
        driver_list = {"default": driver}

        with self.assertRaisesRegex(RuntimeError, "terminate failed"):
            self.run_close(driver_list, system="Darwin")

        self.assertNotIn("default", driver_list)


if __name__ == "__main__":
    unittest.main()
