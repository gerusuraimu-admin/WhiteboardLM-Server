from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.Logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger('Lifespan')
    logger.info(f'Start Callback Server: {app}')

    yield

    logger.info(f'End Callback Server: {app}')
