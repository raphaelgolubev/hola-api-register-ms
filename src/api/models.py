from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.database.mixins import UuidMixin, TimestampMixin


class User(Base, UuidMixin, TimestampMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    user_type: Mapped[str] = mapped_column()


class Profile(Base, UuidMixin, TimestampMixin):
    __tablename__ = 'profiles'

    nickname: Mapped[str] = mapped_column(unique=True)
    birth_date: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()