from contextlib import asynccontextmanager
from fastapi import FastAPI
from .Logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger('Lifespan')
    logger.info(f'Start Login Server: {app}')

    yield

    logger.info(f'End Login Server: {app}')
