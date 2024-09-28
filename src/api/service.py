from src.abstract import Repository, ModelType
from src.repo import SQARepository

from src.api.schemas import RegisterIn
from src.api.exceptions import EmailAlreadyExistsError


class RegisterService:
    def __init__(self, repository: Repository):
        self.repository = repository
    
    async def get_user(self, id):
        return await self.repository.get_one_by(value=id, column="id")

    async def add_user(self, schema: RegisterIn):
        if await self.check_email_exists(schema.email):
            raise EmailAlreadyExistsError(f"Email '{schema.email}' уже сущестувует")

        return await self.repository.create(schema)
    
    async def check_email_exists(self, email: str):
        model = await self.repository.get_one_by(value=email, column="email")
        if model:
            print("check_email_exists", model)
            return True

        return False


def get_service(model: ModelType) -> RegisterService:
    repo = SQARepository(model=model)
    service = RegisterService(repository=repo)

    return service