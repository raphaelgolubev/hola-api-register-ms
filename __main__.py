import uvicorn

from src.config import app_settings
import src.logging # noqa


uvicorn.run(
    'src.application:app',
    host=app_settings.host,
    port=app_settings.port,
    timeout_keep_alive=30,
    lifespan='on',
    reload=True,
)