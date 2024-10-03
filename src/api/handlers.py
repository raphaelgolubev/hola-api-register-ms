import traceback
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
    В случае удачного создания пользователя отправляет код на почту.
    Возвращает id и тип нового пользователя.
    """
    try:
        db_model = await service.add_user(schema=input)
        service.send_email_code(db_model.email)

    except EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким адресом электронной почты уже существует")

    except PhoneAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Пользователь с таким номера телефона уже существует")

    except Exception as e:
        logger.error(f"{e}, {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Неизвестная ошибка")

    else:
        
        return RegisterOut.model_validate(db_model, from_attributes=True)


@router.post(
    "/send_email_code",
    name="Отправка кода на адрес электронной почты",
)
async def send_email_code(user_id: str):
    pass


@router.post(
    "/verify_email_code",
    name="Подтверждение отправленного кода",
)
async def verify_email_code(user_id: str):
    pass
