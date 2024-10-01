from typing import Annotated
from fastapi import Depends

from src.repo import SQARepository
from src.api.service import RegisterService
from src.api.models import User
from src.utils.security import Security


def get_register_service() -> RegisterService:
    repo = SQARepository(model=User)
    service = RegisterService(repository=repo, security=Security())
    return service


RegisterServiceDep = Annotated[RegisterService, Depends(get_register_service)]