from fastapi import FastAPI

from src.database import database
from src.database.tables import create_all, drop_all
from src.utils.ansi_colors import ANSI
from src.routing import main_router

from src.logging import logger

async def startup():
    logger.info("Starting up...")
    try:
        logger.info(f"Connecting to database: {database.url}")
        await database.connect()
        await create_all()
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
    logger.success(f"Connected to database, tables created")


async def shutdown():
    logger.info("Shutting down...")
    try:
        await drop_all()
        logger.info(f"Disconnecting from database")
        await database.disconnect()
    except Exception as e:
        logger.error(f"Error disconnecting from database: {str(e)}")
    logger.success("Disconnected from database")


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix="/api/v1")

@app.get("/ping")
def ping():
    return "pong"