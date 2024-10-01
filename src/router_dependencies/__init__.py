from fastapi import Request

from src.logging import logger


async def log_request(request: Request):
    logger.log("REQUEST", f"Request: {request.method} {request.url}")
    logger.log("REQUEST", f"Client: {request.client.host}:{request.client.port}")
    logger.log("REQUEST", "Params:")
    for name, value in request.path_params.items():
        logger.log("REQUEST", f"\t{name}: {value}")
    logger.log("REQUEST", "Headers:")
    for name, value in request.headers.items():
        logger.log("REQUEST", f"\t{name}: {value}")