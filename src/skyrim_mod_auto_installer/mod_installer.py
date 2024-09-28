import threading
import typing
import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

from .utils import try_find_element
from .tab_driver import TabDriver


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

        self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, "//span[@class='flex-label' and text()='Vortex']").click(),
            task_description=f"[{self.mod_name}] Click the Vortex download button",
            requires_tab_focus_until_end=False,
        )

        if self.do(
            lambda: try_find_element(self.chrome_driver, By.XPATH, "//a[@class='btn' and text()='Download']"),
            task_description=f"[{self.mod_name}] Searching for dependencies",
        ):
            logging.info(f"[{self.mod_name}] Dependencies found")
            self.do(
                lambda: self.chrome_driver.find_element(By.XPATH, "//a[@class='btn' and text()='Download']").click(),
                task_description=f"[{self.mod_name}] Ignoring Dependencies",
            )

        self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, "//span[text()='Slow download']").click(),
            task_description=f"[{self.mod_name}] Click the slow download button",
        )

        self.do(
            lambda: time.sleep(8),
            task_description=f"[{self.mod_name}] Waiting for download",
            requires_tab_focus_until_end=False,
        )

        self.destroy_focus()


class SkyrimModInstallerBySearch(SkyrimModInstaller):
    def __init__(
        self,
        mod_name: str,
        chrome_driver: Chrome,
        *,
        url: str = "https://www.nexusmods.com/skyrimspecialedition/search/",
        driver_lock: typing.Optional[threading.Lock] = None
    ) -> None:
        super().__init__(
            mod_name,
            chrome_driver,
            url=url,
            driver_lock=driver_lock
        )

    def install(self):
        self.init_focus()

        search_icons = self.do(
            lambda: self.chrome_driver.find_elements(By.XPATH, "//i[text()='search']"),
            task_description=f"Retrieving search icons",
        )
        for i, search_icon in enumerate(search_icons, start=1):
            try:
                self.do(
                    lambda: search_icon.click(),
                    task_description=f"Ensuring Search Bar Is Visible {i}"
                )
            except Exception:
                pass

        search_box = self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, '//input[@name="gsearch"]'),
            task_description=f"Finding Search Bar"
        )
        self.do(
            lambda: search_box.send_keys(self.mod_name),
            task_description=f"Typing mod name..."
        )
        search_box = self.do(
            lambda: search_box.send_keys(Keys.RETURN),
            task_description=f"Searching Mod"
        )

        # Trigger the action inside the focus context
        self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, f"//a[text()=\"{self.mod_name}\"]").click(),
            task_description=f"Entering the mod page",
            requires_tab_focus_until_end=False,
        )

        return super().install()
