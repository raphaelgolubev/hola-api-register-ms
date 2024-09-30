from abc import ABC, abstractmethod
from typing import TypeAlias
from pydantic import BaseModel

from src.database import Base


ModelType: TypeAlias = Base
SchemaType: TypeAlias = BaseModel


class IRepository(ABC):
    @abstractmethod
    async def create(self, schema: ModelType):
        raise NotImplementedError

    @abstractmethod
    async def get_one_by(self, value: str, column: str):
        raise NotImplementedError


class ISecurity(ABC):
    @abstractmethod
    def hash_value(self, password: str):
        raise NotImplementedError

    @abstractmethod
    def verify(self, plain: str, hash: str):
        raise NotImplementedError
