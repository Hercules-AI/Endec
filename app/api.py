from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .healthcheck import router as healthcheck_router
from app.endpoints.endec_encoder import router as encoder_router
from app.endpoints.endec_decoder import router as decoder_router


from app.db import connect_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    yield


def init_app():
    router = APIRouter()
    router.include_router(healthcheck_router)
    router.include_router(encoder_router)
    router.include_router(decoder_router)
    

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = init_app()
