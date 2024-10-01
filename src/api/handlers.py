from fastapi import APIRouter, HTTPException

from src.api.schemas import RegisterIn, RegisterOut
from src.api.exceptions import EmailAlreadyExistsError
from src.logging import loguru_logger

from src.api.dependencies import RegisterServiceDep


router = APIRouter()


@loguru_logger.catch
@router.post(
    "/create_user",
    name="Создание нового пользователя",
    response_model=RegisterOut,
)
async def create_user(
    register_data: RegisterIn, 
    service: RegisterServiceDep,
):
    """
    Создание нового пользователя в БД.
    Возвращает id и тип нового пользователя.
    """
    try:
        db_model = await service.add_user(schema=register_data)
        return RegisterOut.model_validate(db_model, from_attributes=True)

    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
