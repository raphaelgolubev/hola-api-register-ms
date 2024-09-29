from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable, DropTable

from src.database import database, Base

# Я импортирую таблицы в этот файл исключительно ради эстетики
# чтобы из любого модуля получать доступ ко всем таблицам с помощью:
# "from src.database.tables import Table1, Table2, Table3,..."
# Это выглядит семантически правильным
from src.api.models import User
from src.api.models import Profile

from src.utils.ansi_colors import ANSI
from src.logging import logger


async def create_all():
    logger.info(ANSI("---  Creating tables ---").purple.bg.end)
    for table in Base.metadata.tables.values():
        logger.info(ANSI(f"Creating table: {table.name}").purple.end)
        schema = CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=postgresql.dialect()))

        await database.execute(query)


async def drop_all():
    logger.info(ANSI("---  Dropping tables ---").purple.bg.end)
    for table in Base.metadata.tables.values():
        logger.info(ANSI(f"Dropping table: {table.name}").purple.end)
        schema = DropTable(table, if_exists=True)
        query = str(schema.compile(dialect=postgresql.dialect()))

        await database.execute(query)
