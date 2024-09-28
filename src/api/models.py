from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.database.mixins import UuidMixin, TimestampMixin


class User(Base, UuidMixin, TimestampMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    user_type: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()