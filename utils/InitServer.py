import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.Lifespan import lifespan


def get_server() -> FastAPI:
    server: FastAPI

    deploy = bool(int(os.environ['DEPLOY']))

    if deploy:
        server = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    else:
        server = FastAPI(lifespan=lifespan)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    return server
