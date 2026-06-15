import logging
import os

LOG_DIR = "src/logs"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("api_logger")

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    f"{LOG_DIR}/api.log"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)