from fastapi import APIRouter, Depends

from src.router_dependencies import log_request
from src.api.handlers import router as register_router


main_router = APIRouter(dependencies=[
    Depends(log_request)
])

main_router.include_router(register_router, prefix='/register', tags=['Register'])