from abc import ABC, abstractmethod
from typing import TypeAlias
from pydantic import BaseModel

from src.database import Base


ModelType: TypeAlias = Base
SchemaType: TypeAlias = BaseModel


class Repository(ABC):
    @abstractmethod
    async def create(self, schema: ModelType):
        raise NotImplementedError

    @abstractmethod
    async def get_one_by(self, value: str, column: str):
        raise NotImplementedError


