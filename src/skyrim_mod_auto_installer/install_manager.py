import os
import psutil
import subprocess
import typing
import threading
import concurrent.futures
import random
import uuid
import shutil

from selenium import webdriver

from .collection_installer import fetch_collection_mod_urls
from .mod_installer import (
    BaseSkyrimModInstaller,
    SkyrimModInstallerBySearch,
    SkyrimModInstallerByURL,
)
from .utils import chunk_list
from . import logger


# Typing definition for a callable that matches the signature of `run_mod_search_installer`
RunModInstallerType = typing.Callable[
    [
        typing.Iterable[str],  # mod_names argument
        typing.Optional[int],  # max_concurrent_tabs_per_browser_instance (keyword-only)
        typing.Optional[str],  # instance_id (keyword-only)
    ],
    None
]

def create_instance_id() -> str:
    return str(uuid.uuid4())


def get_default_chrome_profile_path() -> typing.Tuple[str, str]:
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    # Construct the path to the Chrome user profile
    chrome_profile_path = os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")
    return chrome_profile_path, "Default"


def get_or_create_test_profile(
    instance_id: typing.Optional[str] = None,
) -> typing.Tuple[str, str]:
    profile_path, profile = get_default_chrome_profile_path()
    if instance_id is None:
        return profile_path, profile

    instance_profile = f"{profile}{instance_id}"

    if not os.path.exists(os.path.join(profile_path, instance_profile)):
        # Copy the default profile to the new directory
        shutil.copytree(os.path.join(profile_path, profile), os.path.join(profile_path, instance_profile))
        logger.info(f"Profile copied to {profile_path}")
    else:
        logger.info(f"Using existing profile at {profile_path}")

    return profile_path, instance_profile


def kill_chrome_processes():
    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name']):
        # Check if the process name is 'chrome.exe'
        if process.info['name'].lower() == 'chrome.exe':
            # Terminate the process
            process.terminate()
            logger.info(f"Killed process: {process.info['name']} (PID: {process.info['pid']})")


def start_chrome_with_debugging():
    # Command to start Chrome with remote debugging on port 9222
    subprocess.Popen(["start", "chrome", f"--remote-debugging-port={CHROME_PORT}"], shell=True)
    logger.info(f"Chrome started with remote debugging on port {CHROME_PORT}.")


def debug_chrome(
    instance_id: typing.Optional[str] = None,
    port: typing.Optional[int] = None
) -> webdriver.Chrome:
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


def run_mod_collection_installer(
    collection_url: str,
    *,
    max_browser_instances: typing.Optional[int] = None,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
):
    kill_chrome_processes()

    driver = debug_chrome()

    mod_urls = fetch_collection_mod_urls(
        collection_url,
        driver=driver,
    )

    driver.close()

    return run_mod_installers(
        mod_urls, run_mod_url_installer,
        max_browser_instances=max_browser_instances,
        max_concurrent_tabs_per_browser_instance=max_concurrent_tabs_per_browser_instance,
    )


def run_mod_installers(
    mod_keys: typing.List[str],
    installer_callback: RunModInstallerType,
    *,
    max_browser_instances: typing.Optional[int] = None,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
):
    kill_chrome_processes()

    mods_per_browser_instance = (len(mod_keys) // max_browser_instances) + 1 \
        if max_browser_instances is not None \
        else 1
    mod_names_per_browser = chunk_list(mod_keys, mods_per_browser_instance)

    max_instance_ids = max_browser_instances \
        if max_browser_instances is not None \
        else len(mod_names_per_browser)
    instance_ids = [str(i % max_instance_ids) for i in range(len(mod_names_per_browser))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_browser_instances) as executor:
        for _ in executor.map(
            lambda tuple: installer_callback(
                tuple[1],
                max_concurrent_tabs_per_browser_instance=max_concurrent_tabs_per_browser_instance,
                instance_id=tuple[0],
            ),
            zip(instance_ids, mod_names_per_browser)
        ):
            pass

    return None


def run_mod_url_installer(
    mod_urls: typing.Iterable[str],
    *,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
    instance_id: typing.Optional[str] = None,
):
    return run_mod_installer(
        mod_urls, SkyrimModInstallerByURL,
        max_concurrent_tabs_per_browser_instance=max_concurrent_tabs_per_browser_instance,
        instance_id=instance_id,
    )


def run_mod_search_installer(
    mod_names: typing.Iterable[str],
    *,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
    instance_id: typing.Optional[str] = None,
):
    return run_mod_installer(
        mod_names, SkyrimModInstallerBySearch,
        max_concurrent_tabs_per_browser_instance=max_concurrent_tabs_per_browser_instance,
        instance_id=instance_id,
    )


def run_mod_installer(
    mod_keys: typing.Iterable[str],
    installer_clazz: typing.Type[BaseSkyrimModInstaller],
    *,
    max_concurrent_tabs_per_browser_instance: typing.Optional[int] = None,
    instance_id: typing.Optional[str] = None,
):
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

    # run the installers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_tabs_per_browser_instance) as executor:
        for _ in executor.map(
            lambda mod_name: installer_clazz(
                mod_name, driver,
                driver_lock=driver_lock,
            ).try_install(),
            mod_keys
        ):
            pass

    return None
