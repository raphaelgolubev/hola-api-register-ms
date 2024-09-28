from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from src.database import database
from src.api.models import Base

from src.utils.ansi_colors import ANSI


async def create_all():
    print(ANSI("---  Creating tables ---").purple.bg.end)
    for table in Base.metadata.tables.values():
        print(ANSI(f"Creating table: {table.name}").purple.end)
        schema = CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=postgresql.dialect()))

        await database.execute(query)
