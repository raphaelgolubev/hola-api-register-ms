from databases import Database
from sqlalchemy.orm import DeclarativeBase

from src.config import db_settings


database = Database(db_settings.async_dsn)


class Base(DeclarativeBase):
    pass

