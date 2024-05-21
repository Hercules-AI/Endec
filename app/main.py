import uvicorn

from app.configs.app import settings


def start():
    worker_count = 1
    print("Worker count: ", worker_count)
    uvicorn.run(
        "app.api:app",
        host=settings.app_host,
        port=settings.app_port,
        workers=worker_count,
        # reload=settings.app_env == "dev",
    )


if __name__ == "__main__":
    start()
