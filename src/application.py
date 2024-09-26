from fastapi import FastAPI

from src.utils.ansi_colors import ANSI


async def startup():
    print(f"\n -- {ANSI("Application STARTUP").green.bg.bold.end} -- \n")


async def shutdown():
    print(f"\n -- {ANSI("Application SHUTDOWN").red.bg.bold.end} -- \n")


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return "pong"