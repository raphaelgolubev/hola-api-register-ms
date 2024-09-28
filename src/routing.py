from fastapi import APIRouter

from src.api.handlers import router as register_router


main_router = APIRouter()

main_router.include_router(register_router, prefix='/register', tags=['Register'])