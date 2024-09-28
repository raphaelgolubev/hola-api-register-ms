from fastapi import FastAPI

from src.database import database
from src.database.tables import create_all, drop_all
from src.utils.ansi_colors import ANSI
from src.routing import main_router


async def startup():
    print(f"\n -- {ANSI("Application STARTUP").green.bg.bold.end} -- \n")
    try:
        print(f"Connecting to database: {ANSI(database.url).blue.bold.end}")
        await database.connect()
        await create_all()
    except Exception as e:
        print(f"Error connecting to database: {ANSI(str(e)).red.bold.end}")
    print(f"{ANSI("Connected to database, tables created").green.bold.end}")


async def shutdown():
    print(f"\n -- {ANSI("Application SHUTDOWN").red.bg.bold.end} -- \n")
    try:
        await drop_all()
        print(f"Disconnecting from database: {ANSI(database.url).blue.bold.end}")
        await database.disconnect()
    except Exception as e:
        print(f"Error disconnecting from database: {ANSI(str(e)).red.bold.end}")
    print(f"{ANSI("Disconnected from database").green.bold.end}")


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix="/api/v1")

@app.get("/ping")
def ping():
    return "pong"