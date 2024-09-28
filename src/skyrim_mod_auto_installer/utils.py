import typing

from contextlib import contextmanager
from threading import Lock
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# Define a custom context manager that does nothing if the lock is None
@contextmanager
def optional_lock(lock: typing.Optional[Lock]):
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

def try_find_element(
    driver: webdriver.Chrome,
    by: By,
    value: typing.Optional[str],
):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None  # or return a specific value or raise a custom exception
    
def chunk_list(
    input_list: typing.List[typing.Any],
    chunk_size: typing.Optional[int] = None
):
    if chunk_size is None:
        chunk_size = len(input_list)

    # Splitting the list into chunks of size x
    return [
        input_list[i:i + chunk_size]
        for i in range(0, len(input_list), chunk_size)
    ]
