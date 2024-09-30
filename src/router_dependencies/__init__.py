from fastapi import Request

from src.logging import logger


async def log_request(request: Request):
    logger.request(f"Request: {request.method} {request.url}")
    logger.request(f"Client: {request.client.host}:{request.client.port}")
    logger.request("Params:")
    for name, value in request.path_params.items():
        logger.request(f"\t{name}: {value}")
    logger.request("Headers:")
    for name, value in request.headers.items():
        logger.request(f"\t{name}: {value}")