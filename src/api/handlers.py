from fastapi import APIRouter, Request, HTTPException

from src.database.tables import User

from src.api.schemas import RegisterIn, RegisterOut
from src.api.service import get_service
from src.api.exceptions import EmailAlreadyExistsError
from src.logging import loguru_logger


router = APIRouter()


@loguru_logger.catch
@router.post(
    "/sign_up",
    name="Создание нового пользователя",
    response_model=RegisterOut,
)
async def sign_up(register_data: RegisterIn, request: Request):
    """
    Регистрация нового пользователя.
    Возвращает id и тип нового пользователя.
    """
    service = get_service(model=User)

    try:
        db_model = await service.add_user(schema=register_data)
        return RegisterOut.model_validate(db_model, from_attributes=True)

    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
