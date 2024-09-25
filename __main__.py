import uvicorn


uvicorn.run(
    'src.application:app',
    host='0.0.0.0',
    port=8000,
    timeout_keep_alive=30,
    lifespan='on',
)