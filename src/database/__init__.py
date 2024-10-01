from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import db_settings


engine = create_async_engine(db_settings.async_dsn, echo=True)
# database = Database(db_settings.async_dsn)


class Base(DeclarativeBase):
    pass

