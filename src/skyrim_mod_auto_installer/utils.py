from contextlib import contextmanager
from threading import Lock
from typing import Optional
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Define a custom context manager that does nothing if the lock is None
@contextmanager
def optional_lock(lock: Optional[Lock]):
    """
    Sometimes we need a lock, sometimes we don't.
    This function enables a lock to be used only only if it is not None.

    Usage:
    ```python
        def foo(
            lock: Optional[threading.Lock] = None,
            *args,
            **kwargs
        ):
            with optional_lock(lock):
                bar()
    ```
    """
    if lock:
        with lock:
            yield
    else:
        yield

def try_find_element(driver: webdriver.Chrome, by: By, value: Optional[str]):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None  # or return a specific value or raise a custom exception
