# limpieza_data/logger.py

import logging
from limpieza_data.config import LOG_NAME
from pathlib import Path
from datetime import datetime

LOGS_DIR = Path("data/outputs/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_LOG_FILE = LOGS_DIR / f"{LOG_NAME}_{datetime.now().strftime('%Y%m%d')}.log"


def init_logger(name: str = LOG_NAME, log_file: Path = DEFAULT_LOG_FILE, level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
    formatter = logging.Formatter(fmt)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# Helpers
logger = init_logger()


def log_info(logger_obj, msg: str):
    logger_obj.info(msg)


def log_warning(logger_obj, msg: str):
    logger_obj.warning(msg)


def log_error(logger_obj, msg: str):
    logger_obj.error(msg)


def log_debug(logger_obj, msg: str):
    logger_obj.debug(msg)
