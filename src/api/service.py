from src.interfaces import IRepository, ISecurity

from src.repo import SQARepository
from src.database.tables import User, Profile
from src.api.schemas import RegisterIn
from src.api.exceptions import EmailAlreadyExistsError, PhoneAlreadyExistsError

from src.logging import logger
from src.utils.smtp import send_verification_code


class RegisterService:
    def __init__(self, security: ISecurity):
        self.user_repo: IRepository = SQARepository(User)
        self.profile_repo: IRepository = SQARepository(Profile)
        self.security = security

    async def check_email_exists(self, email: str):
        model = await self.user_repo.get_one_by(value=email, column="email")
        if model:
            logger.debug(f"email '{email}' exists")
            return True

        return False

    async def check_phone_exists(self, phone: str):
        model = await self.user_repo.get_one_by(value=phone, column="phone")
        if model:
            logger.debug(f"phone '{phone}' exists")
            return True

        return False

    async def add_user(self, schema: RegisterIn):
        if await self.check_email_exists(schema.email):
            raise EmailAlreadyExistsError(f"Email '{schema.email}' уже сущестувует")

        if await self.check_phone_exists(schema.phone):
            raise PhoneAlreadyExistsError(f"Phone '{schema.phone}' уже существует")

        schema.password = self.security.hash_value(schema.password)
        created_user = await self.user_repo.create(schema)

        profile = Profile()
        profile.user_id = created_user.id
        created_user.profile = profile

        created_user = await self.user_repo.add_and_commit(created_user)

        return created_user

    def send_email_code(self, to_email: str):
        send_verification_code(recipient=to_email, code=123456)

    def verify_email_code(self):
        pass
