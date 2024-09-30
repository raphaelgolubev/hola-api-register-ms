import sys
from loguru import logger


RECORD_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level.icon} <level>{level: <8}</level> | {file.path} | {module}:{line} | {function} | <level>{message}</level>"
ROTATION = "10 MB"
RETENTION = "7 days"
COMPRESSION = "zip"

logger.remove()
logger.add(sys.stderr, level="DEBUG", format=RECORD_FORMAT)

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

logger.add(
    sink="logs/info.json",
    level="INFO",
    filter=lambda record: record["level"].name == "INFO",
    **params,
)

logger.add(
    sink="logs/info.json",
    level="SUCCESS",
    filter=lambda record: record["level"].name == "SUCCESS",
    **params,
)

logger.add(
    sink="logs/error.json",
    level="ERROR",
    filter=lambda record: record["level"].name == "ERROR",
    **params,
)