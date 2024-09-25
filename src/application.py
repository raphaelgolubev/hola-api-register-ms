from fastapi import FastAPI

from src.utils.ansi_colors import Colors, colorize


def _colored_print(shutdown: bool = False, startup: bool = False):
    msg = ''
    if startup:
        msg = colorize("STARTUP", Colors.LIGHT_GREEN)
    else:
        msg = colorize("SHUTDOWN", Colors.LIGHT_RED)
    print(f" -- Application {msg} event has been triggered -- ")


async def startup():
    _colored_print(startup=True)


async def shutdown():
    _colored_print(shutdown=True)


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return "pong"