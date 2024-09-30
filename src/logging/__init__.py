import sys

from typing import Any
from loguru import logger as loguru_logger


loguru_logger.remove()

RECORD_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level.icon} <level>{level: <8}</level> | {file.path} | {module}:{line} | {function} | <level>{message}</level>"
ROTATION = "10 MB"
RETENTION = "7 days"
COMPRESSION = "zip"

# functions
def add(path: str, level: str):
    loguru_logger.add(
        sink=path,
        level=level.upper(),
        filter=lambda record: record["level"].name == level.upper(),
        **params,
    )

# Params
params = {
    "rotation": ROTATION,
    "retention": RETENTION,
    "compression": COMPRESSION,
    "format": RECORD_FORMAT,
    "colorize": None,
    "backtrace": True,
    "serialize": True,
    "diagnose": False,
}

# Custom levels
loguru_logger.level("REQUEST", no=15, color="<blue>", icon="📩")

# Standard output sinks
loguru_logger.add(sys.stderr, level="DEBUG", format=RECORD_FORMAT)

# File sinks
add("logs/request.json", "REQUEST")
add("logs/info.json", "INFO")
add("logs/info.json", "SUCCESS")
add("logs/error.json", "ERROR")


class Logger:
    def __init__(self):
        pass

    def trace(self, *args: Any, **kwargs: Any):
        loguru_logger.trace(*args, **kwargs)

    def debug(self, *args: Any, **kwargs: Any):
        loguru_logger.debug(*args, **kwargs)

    def info(self, *args: Any, **kwargs: Any):
        loguru_logger.info(*args, **kwargs)

    def success(self, *args: Any, **kwargs: Any):
        loguru_logger.success(*args, **kwargs)

    def warning(self, *args: Any, **kwargs: Any):
        loguru_logger.warning(*args, **kwargs)

    def error(self, *args: Any, **kwargs: Any):
        loguru_logger.error(*args, **kwargs)

    def critical(self, *args: Any, **kwargs: Any):
        loguru_logger.critical(*args, **kwargs)
    
    def request(self, *args: Any, **kwargs: Any):
        loguru_logger.log("REQUEST", *args, **kwargs)


logger = Logger()
