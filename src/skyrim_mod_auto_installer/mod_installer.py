import threading
import typing
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

from .utils import try_find_element
from .tab_driver import TabDriver
from . import logger


class BaseSkyrimModInstaller(TabDriver):
    """
    Install a mod from NexusMods using Vortex. Assumes that the
    provided chrome diver is already authenticated, hence the
    login part is skipped.
    """
    def __init__(
        self,
        chrome_driver: Chrome,
        *,
        mod_name: str = "",
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
        # try the install
        try:
            self.install()
        except Exception as e:
            logger.exception(f"Unable to install {self.mod_name}: {e}")

        # if install fails, we should still try
        # to clean up the browser session
        try:
            self.destroy_focus()
        except Exception:
            pass

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
            logger.info(f"[{self.mod_name}] Dependencies found")
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


class SkyrimModInstallerByURL(BaseSkyrimModInstaller):
    def __init__(
        self,
        url: str,
        chrome_driver: Chrome,
        *,
        mod_name: str = "",
        driver_lock: typing.Optional[threading.Lock] = None
    ) -> None:
        super().__init__(
            chrome_driver,
            mod_name=mod_name or url,
            url=url,
            driver_lock=driver_lock,
        )


class SkyrimModInstallerBySearch(BaseSkyrimModInstaller):
    def __init__(
        self,
        mod_name: str,
        chrome_driver: Chrome,
        *,
        url: str = "https://www.nexusmods.com/skyrimspecialedition/search/",
        driver_lock: typing.Optional[threading.Lock] = None
    ) -> None:
        super().__init__(
            chrome_driver,
            mod_name=mod_name,
            url=url,
            driver_lock=driver_lock,
        )

    def install(self):
        self.init_focus()

        search_icons = self.do(
            lambda: self.chrome_driver.find_elements(By.XPATH, "//i[text()='search']"),
            task_description=f"[{self.mod_name}] Retrieving search icons",
        )
        for i, search_icon in enumerate(search_icons, start=1):
            try:
                self.do(
                    lambda: search_icon.click(),
                    task_description=f"[{self.mod_name}] Ensuring Search Bar Is Visible {i}"
                )
            except Exception:
                pass

        search_box = self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, '//input[@name="gsearch"]'),
            task_description=f"[{self.mod_name}] Finding Search Bar"
        )
        self.do(
            lambda: search_box.send_keys(self.mod_name),
            task_description=f"[{self.mod_name}] Typing mod name..."
        )
        search_box = self.do(
            lambda: search_box.send_keys(Keys.RETURN),
            task_description=f"[{self.mod_name}] Searching Mod"
        )

        # Trigger the action inside the focus context
        self.do(
            lambda: self.chrome_driver.find_element(By.XPATH, f"//a[text()=\"{self.mod_name}\"]").click(),
            task_description=f"[{self.mod_name}] Entering the mod page",
            requires_tab_focus_until_end=False,
        )

        return super().install()
