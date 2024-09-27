import threading
import typing
import time
import logging

from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

from .utils import optional_lock, try_find_element


class TabDriver():
    """
    An interace that enables control of a single tab in a browser.
    This is thread safe, meaning multiple TabDrivers can perform on
    the same Chrome Driver instance.
    """
    def __init__(
        self,
        chrome_driver: Chrome,
        *,
        url: str = "",
        driver_lock: typing.Optional[threading.Lock] = None,
    ) -> None:
        self.chrome_driver = chrome_driver
        self.url = url
        self.driver_lock = driver_lock
        self.focus_id = None

    def init_focus(self) -> None:
        with optional_lock(self.driver_lock):
            self.chrome_driver.execute_script(f"window.open('{self.url}');")
            self.focus_id = self.chrome_driver.window_handles[-1]

    @contextmanager
    def focus(self):
        with optional_lock(self.driver_lock):
            self.chrome_driver.switch_to.window(self.focus_id)
            yield


class SkyrimModInstaller(TabDriver):
    """
    Install a mod from NexusMods using Vortex. Assumes that the
    provided chrome diver is already authenticated, hence the
    login part is skipped.
    """
    def __init__(
        self,
        mod_name: str,
        chrome_driver: Chrome,
        *,
        url: str = "",
        driver_lock: typing.Optional[threading.Lock] = None,
    ) -> None:
        super().__init__(
            chrome_driver=chrome_driver,
            url=url,
            driver_lock=driver_lock,
        )
        self.mod_name = mod_name

    def try_install(self):
        try:
            self.install()
        except Exception as e:
            logging.exception(f"Unable to install {self.mod_name}: {e}")

    def install(self):
        self.init_focus()

        logging.info(f"[{self.mod_name}] Open the Nexus Mods search page")
        with self.focus():
            self.chrome_driver.get("https://www.nexusmods.com/skyrimspecialedition/search/")
        time.sleep(2)

        logging.info(f"[{self.mod_name}] Find the search box and enter the mod name")
        with self.focus():
            search_icons = self.chrome_driver.find_elements(By.XPATH, "//i[text()='search']")
            if search_icons:
                for search_icon in search_icons:
                    try:
                        search_icon.click()
                    except Exception:
                        pass
                time.sleep(1)
            search_box = self.chrome_driver.find_element(By.XPATH, '//input[@name="gsearch"]')
            search_box.send_keys(self.mod_name)
            search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        logging.info(f"[{self.mod_name}] Click on the first result")
        with self.focus():
            first_result = self.chrome_driver.find_element(By.XPATH, f"//a[text()=\"{self.mod_name}\"]")
            first_result.click()
        time.sleep(1)

        logging.info(f"[{self.mod_name}] click the vortex download button")
        with self.focus():
            vortex_download_button = self.chrome_driver.find_element(By.XPATH, "//span[@class='flex-label' and text()='Vortex']")
            vortex_download_button.click()
        time.sleep(1)

        if try_find_element(self.chrome_driver, By.XPATH, "//a[@class='btn' and text()='Download']"):
            logging.info(f"[{self.mod_name}] dependencies found")
            with self.focus():
                ctn_download_button = self.chrome_driver.find_element(By.XPATH, "//a[@class='btn' and text()='Download']")
                ctn_download_button.click()
            time.sleep(1)

        logging.info(f"[{self.mod_name}] click the slow download button")
        with self.focus():
            slow_download_button = self.chrome_driver.find_element(By.XPATH, "//span[text()='Slow download']")
            slow_download_button.click()
        time.sleep(6)
