import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("motimate")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler("logs/motimate.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Terminal handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(file_formatter)
    logger.addHandler(stream_handler)