from src.abstract import Repository, ModelType
from src.repo import SQARepository

from src.api.schemas import RegisterIn
from src.api.exceptions import EmailAlreadyExistsError, PhoneAlreadyExistsError

from src.logging import logger


class RegisterService:
    def __init__(self, repository: Repository):
        self.repository = repository


    async def get_user(self, id):
        return await self.repository.get_one_by(value=id, column="id")


    async def add_user(self, schema: RegisterIn):
        if await self.check_email_exists(schema.email):
            raise EmailAlreadyExistsError(f"Email '{schema.email}' уже сущестувует")

        if await self.check_phone_exists(schema.phone):
            raise PhoneAlreadyExistsError(f"Phone '{schema.phone}' уже существует")

        return await self.repository.create(schema)


    async def check_email_exists(self, email: str):
        model = await self.repository.get_one_by(value=email, column="email")
        if model:
            logger.debug("email exists")
            return True

        return False


    async def check_phone_exists(self, phone: str):
        model = await self.repository.get_one_by(value=phone, column="phone")
        if model:
            logger.debug("phone exists")
            return True

        return False


def get_service(model: ModelType) -> RegisterService:
    repo = SQARepository(model=model)
    service = RegisterService(repository=repo)

    return service