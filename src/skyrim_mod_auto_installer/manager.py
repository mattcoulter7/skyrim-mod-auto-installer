import time
import psutil
import subprocess
import typing
import logging
import threading
import concurrent.futures
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from .mod_installer import SkyrimModInstaller, SkyrimModInstallerBySearch
from .constants import CHROME_PORT


def kill_chrome_processes():
    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name']):
        # Check if the process name is 'chrome.exe'
        if process.info['name'].lower() == 'chrome.exe':
            # Terminate the process
            process.terminate()
            logging.info(f"Killed process: {process.info['name']} (PID: {process.info['pid']})")


def start_chrome_with_debugging():
    # Command to start Chrome with remote debugging on port 9222
    subprocess.Popen(["start", "chrome", f"--remote-debugging-port={CHROME_PORT}"], shell=True)
    logging.info(f"Chrome started with remote debugging on port {CHROME_PORT}.")


def debug_chrome() -> webdriver.Chrome:
    # Initialize the WebDriver (make sure to specify the path if it's not in your PATH)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_PORT}")

    # Initialize the WebDriver with the existing session
    return webdriver.Chrome(options=chrome_options)


def run_installer(
    mod_names: typing.List[str],
    *,
    max_workers: typing.Optional[int] = None,
    shuffle: bool = False,
):
    if shuffle:
        random.shuffle(mod_names)

    # prepare the chrome driver
    kill_chrome_processes()
    start_chrome_with_debugging()
    time.sleep(2)
    driver = debug_chrome()

    # create lock for tab management 
    driver_lock = threading.Lock()

    # prepare the installer objects
    mod_installers = [
        SkyrimModInstallerBySearch(
            mod_name=mod_name,
            chrome_driver=driver,
            driver_lock=driver_lock,
        )
        for mod_name in mod_names
    ]

    # run the installers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(
            lambda mod_installer: mod_installer.install(),
            mod_installers
        ):
            pass

    return None
