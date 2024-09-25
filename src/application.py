from fastapi import FastAPI

from src.utils.ansi_colors import ANSI


async def startup():
    print(ANSI("\n -- Application STARTUP event has been triggered -- \n").yellow())


async def shutdown():
    print(ANSI("\n -- Application STARTUP event has been triggered -- \n").light_red())


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return "pong"