from typing import Any, Dict
from pydantic import BaseModel


class AuthPayload(BaseModel):
    uid: str
    session_id: str


class LoginPayload(BaseModel):
    username: str
    password: str


class LogoutPayload(BaseModel):
    session_id: str


class RegisterPayload(BaseModel):
    username: str
    password: str


class Response(BaseModel):
    status_code: int
    content: Dict[str, Any]
