import threading
import typing
import queue
import time

from contextlib import contextmanager
from selenium.webdriver import Chrome
from concurrent.futures import ThreadPoolExecutor

from .utils import optional_lock
from . import logger

# Define a global ThreadPoolExecutor with a limited number of threads
MAX_THREADS = 128  # You can adjust this based on your requirements
global_executor = ThreadPoolExecutor(max_workers=MAX_THREADS)

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
        self.init = False

    def init_focus(self) -> None:
        # only runs init once
        if self.focus_id:
            return

        with optional_lock(self.driver_lock):
            self.chrome_driver.execute_script(f"window.open('');")  # don't use url here as it doesn't wait
            self.focus_id = self.chrome_driver.window_handles[-1]

        if self.url:
            self.do(
                lambda: self.chrome_driver.get(self.url),
                task_description=f"Navigating to url: `{self.url}`",
                requires_tab_focus_until_end=False,
            )

    def destroy_focus(self) -> None:
        # Closes the tab with the current focus_id if it exists
        if not self.focus_id:
            return
        
        with optional_lock(self.driver_lock):
            # Switch to the tab to ensure it's the one being closed
            self.chrome_driver.switch_to.window(self.focus_id)
            # Close the current tab
            self.chrome_driver.close()
            # Reset the focus_id as the tab is now closed
            self.focus_id = None
            # Set current windows to first valid window
            self.chrome_driver.switch_to.window(self.chrome_driver.window_handles[0])

    @contextmanager
    def focus(
        self,
        block: bool = True,
    ):
        if block:
            with optional_lock(self.driver_lock):
                self.chrome_driver.switch_to.window(self.focus_id)
                yield
        else:
            yield

    def do(
        self,
        task: typing.Callable[[], typing.Any],
        task_description: typing.Optional[str] = None,
        *,
        requires_tab_focus_until_end: bool = True,
        tab_active_threshold: float = 0.5,
    ) -> typing.Any:
        # Create a queue to capture the result from the executor
        result_queue = queue.Queue()

        about_to_begin_event = threading.Event()

        # Wrap the task to put the result in the queue
        def wrapped_task():
            try:
                about_to_begin_event.set()
                result = task()
                result_queue.put(result)
            except Exception as e:
                result_queue.put(e)  # Put the exception in the queue to handle it later

        # begin the task with tab focus
        if task_description:
            logger.info(f"TASK BEGIN: {task_description}")
        with self.focus():
            # Submit the task to the global thread pool executor
            future = global_executor.submit(wrapped_task)
            about_to_begin_event.wait()
            time.sleep(tab_active_threshold)  # short sleep to ensure execution has actually started, don't want to tab to move away without actually starting the event

        # finish the task with tab focus
        if task_description:
            logger.info(f"TASK IN PROGRESS: {task_description}")
        with self.focus(requires_tab_focus_until_end):
            future.result()  # Wait for the task to complete

        if task_description:
            logger.info(f"TASK COMPLETED: {task_description}")

        result = result_queue.get()
        if isinstance(result, Exception):
            raise result  # Re-raise the exception or handle it as needed
        return result
