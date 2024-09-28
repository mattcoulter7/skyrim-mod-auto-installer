import threading
import typing
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from diskcache import Cache

from .utils import try_find_element
from .tab_driver import TabDriver

cache = Cache(".skyrim-mod-auto-installer_cache")


def fetch_collection_mod_urls(
    collection_url: str,
    driver: Chrome,
) -> typing.Generator[str, None, None]:
    @cache.memoize()
    def iteratively_find_urls(collection_url: str):
        mod_urls = []

        driver.get(collection_url)

        mods_tab = driver.find_element(
            By.XPATH, '//button[@aria-controls="tabcontent-mods"]'
        )
        mods_tab.click()
        time.sleep(5)

        mod_labels = driver.find_elements(
            By.XPATH, '//div[@class="collection-mod-row__mod-name-container"]/span'
        )
        for mod_label in mod_labels:
            # Create an instance of ActionChains
            action = ActionChains(driver)

            # Perform the hover action
            action.move_to_element(mod_label).perform()

            # find the mod anchor
            mod_anchor = driver.find_element(
                By.XPATH, f"//a[contains(@href, 'https://www.nexusmods.com/skyrimspecialedition/mods/')]"
            )

            mod_link = mod_anchor.get_property("href")

            mod_urls.append(mod_link)
        
        return mod_urls

    return iteratively_find_urls(collection_url)