from fastapi import APIRouter, HTTPException

from src.api.schemas import RegisterIn, RegisterOut
from src.api.exceptions import EmailAlreadyExistsError, PhoneAlreadyExistsError
from src.logging import logger

from src.api.dependencies import RegisterServiceDep


router = APIRouter()


@logger.catch
@router.post(
    "/create_user",
    name="Создание нового пользователя",
    response_model=RegisterOut,
)
async def create_user(input: RegisterIn, service: RegisterServiceDep):
    """
    Создание нового пользователя в БД.
    Возвращает id и тип нового пользователя.
    """
    try:
        db_model = await service.add_user(schema=input)
        return RegisterOut.model_validate(db_model, from_attributes=True)

    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким адресом электронной почты уже существует")
    
    except PhoneAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким номера телефона уже существует")
