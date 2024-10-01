from typing import Annotated
from fastapi import Depends

from src.api.service import RegisterService
from src.utils.security import Security


def get_register_service() -> RegisterService:
    security = Security()
    service = RegisterService(security=security)
    return service


RegisterServiceDep = Annotated[RegisterService, Depends(get_register_service)]