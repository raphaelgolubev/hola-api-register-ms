from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    user_type: Mapped[str] = mapped_column()