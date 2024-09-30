from sqlalchemy import Table
from uuid import UUID

from src.interfaces import IRepository, ModelType, SchemaType
from src.database import database
from src.utils.ansi_colors import ANSI
from src.logging import logger


class SQARepository(IRepository):
    def __init__(self, model: ModelType):
        self.model = model
        self.table = Table(
            self.model.__tablename__, 
            self.model.metadata, 
            autoload=True
        )

    async def _retrieve(self, id: str):
        """ 
        Выполняет запрос `SELECT * FROM <table> WHERE id = :id` для текущей таблицы.
        Потому что метод `database.execute` не умеет 
        работать с `.returning()` модуля SQLAlchemy,
        а именно возвращать более чем один столбец.
        """
        select = f"SELECT * FROM {self.model.__tablename__} WHERE id = :id"
        record = await database.fetch_one(query=select, values={"id": id})

        return record

    async def create(self, schema: SchemaType):
        query = self.table.insert()
        query = query.values(**schema.model_dump())
        query = query.returning(self.table.c.id)

        logger.debug(ANSI(f"{query};\nUsing values: {query.compile().params}").purple.end.replace("\n", ""))

        id = await database.execute(query=query)
        record = await self._retrieve(id=id)

        if record:
            return self.model(**record)

        return None

    async def create_many(self, schemas: list[SchemaType]):
        table = Table(self.model.__tablename__, self.model.metadata, autoload=True)
        query = table.insert()

        logger.debug(ANSI(f"Making INSERT: {query}; Using many values").purple.end.replace("\n", ""))

        values = [schema.model_dump() for schema in schemas]
        await database.execute_many(query=query, values=values)

    async def get_one_by(self, value: str, column: str):
        query = self.table.select()
        query = query.where(getattr(self.table.c, column) == value)

        logger.debug(ANSI(f"Making SELECT: {query}; Where {column} = {value}").purple.end.replace("\n", ""))

        record = await database.fetch_one(query=query)
        
        if record:
            return self.model(**record)

        return None

    async def get_many_by_id(self, ids: list[str | UUID], column: str = "id"):
        table = Table(self.model.__tablename__, self.model.metadata, autoload=True)
        query = table.select().where(getattr(table.c, column).in_(ids))

        logger.debug(ANSI(f"Making SELECT: {query}; Using ids: {ids}").purple.end.replace("\n", ""))

        await database.fetch_many(query=query)