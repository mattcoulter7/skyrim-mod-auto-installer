import os
import time
import psutil
import subprocess
import typing
import logging
import threading
import concurrent.futures
import random
import uuid
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from .mod_installer import SkyrimModInstaller, SkyrimModInstallerBySearch
from .constants import CHROME_PORT
from .utils import chunk_list


def create_instance_id() -> str:
    return str(uuid.uuid4())


def get_default_chrome_profile_path() -> typing.Tuple[str, str]:
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    # Construct the path to the Chrome user profile
    chrome_profile_path = os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")
    return chrome_profile_path, "Default"


def get_or_create_test_profile(instance_id: str) -> typing.Tuple[str, str]:
    profile_path, profile = get_default_chrome_profile_path()

    # Create a unique directory for each instance's profile
    # home_dir = os.path.expanduser("~")
    instance_profile_path = profile_path  # os.path.join(home_dir, f".skyrim-mod-auto-installer")
    instance_profile = f"{profile}{instance_id}"

    if not os.path.exists(os.path.join(instance_profile_path, instance_profile)):
        # Copy the default profile to the new directory
        shutil.copytree(os.path.join(profile_path, profile), os.path.join(instance_profile_path, instance_profile))
        logging.info(f"Profile copied to {instance_profile_path}")
    else:
        logging.info(f"Using existing profile at {instance_profile_path}")

    return instance_profile_path, instance_profile


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


def debug_chrome(instance_id: str, port: int = None) -> webdriver.Chrome:
    profile_path, profile = get_or_create_test_profile(instance_id)

    # Generate a random port if none is provided to avoid conflicts
    if port is None:
        port = random.randint(9223, 65535)  # Choose a port range above 9222 to avoid conflicts

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument(f"--profile-directory={profile}")
    chrome_options.add_argument(f"--remote-debugging-port={port}")

    # Initialize the WebDriver with the specified port
    return webdriver.Chrome(options=chrome_options)


def run_installers(
    mod_names: typing.List[str],
    *,
    max_browser_instances: typing.Optional[int] = None,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
):
    kill_chrome_processes()

    mods_per_browser_instance = (len(mod_names) // max_browser_instances) + 1 \
        if max_browser_instances is not None \
        else 1
    mod_names_per_browser = chunk_list(mod_names, mods_per_browser_instance)

    max_instance_ids = max_browser_instances \
        if max_browser_instances is not None \
        else len(mod_names_per_browser)
    instance_ids = [str(i % max_instance_ids) for i in range(len(mod_names_per_browser))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_browser_instances) as executor:
        for _ in executor.map(
            lambda tuple: run_installer(
                mod_names=tuple[1],
                max_tabs_per_browser_instance=max_concurrent_tabs_per_browser_instance,
                instance_id=tuple[0],
            ),
            zip(instance_ids, mod_names_per_browser)
        ):
            pass

    return None


def run_installer(
    mod_names: typing.List[str],
    *,
    max_tabs_per_browser_instance: typing.Optional[int] = None,
    instance_id: typing.Optional[str] = None,
):
    instance_id = instance_id or create_instance_id()

    # legacy approach to get the authenticated chrome with nexus mods was
    # by using shell which automatically used the default profile.
    # this was limited to a single browser, but we can actually include
    # the profile in ChromeOptions, hence supporting multiple browsers.
    # start_chrome_with_debugging()
    # time.sleep(2)
    driver = debug_chrome(
        instance_id=instance_id,
    )

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_tabs_per_browser_instance) as executor:
        for _ in executor.map(
            lambda mod_installer: mod_installer.install(),
            mod_installers
        ):
            pass

    return None
