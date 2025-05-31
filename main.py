from logging import Logger
from fastapi import FastAPI

from utils import get_logger, get_server, Session
from utils import (
    handle_wrapper,
    handle_auth,
    handle_login,
    handle_logout,
    handle_register,
    handle_embed,
    handle_query,
    AuthPayload,
    LoginPayload,
    LogoutPayload,
    RegisterPayload,
    QueryPayload
)

logger: Logger = get_logger(__name__)
server: FastAPI = get_server()
session: Session = Session()

@server.post('/auth')
@handle_wrapper
async def auth(payload: AuthPayload):
    logger.info('Auth request')
    return handle_auth(payload, session)


@server.post('/login')
@handle_wrapper
async def login(payload: LoginPayload):
    logger.info('Login request')
    return handle_login(payload, session)


@server.post('/logout')
@handle_wrapper
async def logout(payload: LogoutPayload):
    logger.info('Logout request')
    return handle_logout(payload, session)


@server.post('/register')
@handle_wrapper
async def register(payload: RegisterPayload):
    logger.info('Register request')
    return handle_register(payload)


@server.post('/embed')
@handle_wrapper
async def embed(payload: AuthPayload):
    logger.info('Embed request')
    return handle_embed(payload, session)


@server.post('/query')
@handle_wrapper
async def query(payload: QueryPayload):
    logger.info('Query request')
    return handle_query(payload)
