from fastapi import FastAPI


app = FastAPI()


async def startup():
    print("Application STARTUP event has been triggered")


async def shutdown():
    print("Application SHUTDOWN event has been triggered")


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


@app.get("/ping")
def ping():
    return "pong"