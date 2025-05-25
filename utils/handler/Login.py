import os
import requests
from typing import Dict
from utils.Session import Session
from utils.Payload import LoginPayload, Response

"""
LoginPayload:
    email: str
    password: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'uid': uid,
    'session_id': session_id,
    'message': message
}
"""


class InvalidLoginError(Exception):
    pass


def handle_login(payload: LoginPayload) -> Response:
    try:
        return Response(status_code=200, content=get_content(payload))

    except InvalidLoginError:
        return Response(status_code=401, content={'message': f'Failed to login'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def get_content(payload: LoginPayload) -> Dict[str, str]:
    response = login_request(payload)
    uid = response.get("localId")

    session = Session()
    session_id = session.login(uid, response.get("refreshToken"))
    message = 'Login Successful'

    content = {
        'uid': uid,
        'session_id': session_id,
        'message': message
    }

    return content


def login_request(payload: LoginPayload) -> Dict[str, str]:
    api_key = os.environ['API_KEY']
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    auth_payload = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=auth_payload)
    if response.status_code != 200:
        raise InvalidLoginError()

    return response.json()
