from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .Lifespan import lifespan


def get_server() -> FastAPI:
    server = FastAPI(lifespan=lifespan)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return server
