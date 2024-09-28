# src/logging_config.py
import logging
import os
from datetime import datetime

# Define log directory
log_dir = os.path.join(os.path.expanduser("~"), ".skyrim-mod-auto-installer", "logs")
os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # e.g., 2024-09-28_14-30-45
log_file = os.path.join(log_dir, f"{timestamp}.log")  # Log file with timestamp

# Basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] - %(name)s - %(message)s",  # Include module name with %(name)s
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(log_file),  # Log to file
    ],
)

# Get the root logger
logger = logging.getLogger(__name__)
logger.info("Logging is set up.")
