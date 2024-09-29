import sys
from loguru import logger

from src.utils.ansi_colors import ANSI


RECORD_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level.icon} <level>{level: <8}</level> | {file.path} | {module}:{line} | {function} | <level>{message}</level>"
ROTATION = "10 MB"
RETENTION = "7 days"
COMPRESSION = "zip"


def info_only(record):
    return record["level"].name == "INFO"

def success_only(record):
    return record["level"].name == "SUCCESS"

def error_only(record):
    return record["level"].name == "ERROR"


logger.remove()

logger.add(sys.stderr, level="DEBUG", format=RECORD_FORMAT)
logger.add(sys.stdout, level="INFO", format=RECORD_FORMAT)
logger.add(sys.stdout, level="SUCCESS", format=RECORD_FORMAT)
logger.add(sys.stdout, level="ERROR", format=RECORD_FORMAT)

logger.add(
    "logs/info.json",
    level="INFO",

    rotation=ROTATION,
    retention=RETENTION,
    compression=COMPRESSION,
    format=RECORD_FORMAT,
    filter=info_only,

    colorize=True,
    backtrace=True,
    serialize=True,
)

logger.add(
    "logs/info.json",
    level="SUCCESS",

    rotation=ROTATION,
    retention=RETENTION,
    compression=COMPRESSION,
    format=RECORD_FORMAT,
    filter=success_only,

    colorize=True,
    backtrace=True,
    serialize=True,
)

logger.add(
    "logs/error.json",
    level="ERROR",

    rotation=ROTATION,
    retention=RETENTION,
    compression=COMPRESSION,
    format=RECORD_FORMAT,
    filter=error_only,

    colorize=True,
    backtrace=True,
    serialize=True,
)