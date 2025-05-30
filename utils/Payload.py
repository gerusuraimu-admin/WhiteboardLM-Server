from typing import Any, Dict
from pydantic import BaseModel


class AuthPayload(BaseModel):
    uid: str
    session_id: str


class LoginPayload(BaseModel):
    email: str
    password: str


class LogoutPayload(BaseModel):
    uid: str
    session_id: str


class RegisterPayload(BaseModel):
    email: str
    password: str


class Response(BaseModel):
    status_code: int
    content: Dict[str, Any]


class QueryPayload(BaseModel):
    uid: str
    message: str
