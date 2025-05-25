import os
import requests
from typing import Dict
from google.cloud import storage
from utils.Payload import RegisterPayload, Response

"""
RegisterPayload:
    email: str
    password: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'message': message
}
"""


class InvalidRegisterError(Exception):
    pass


class FailedCreateDirectory(Exception):
    pass


def handle_register(payload: RegisterPayload) -> Response:
    try:
        return Response(status_code=200, content=get_content(payload))

    except InvalidRegisterError:
        return Response(status_code=401, content={'message': f'Failed to register'})

    except FailedCreateDirectory:
        return Response(status_code=500, content={'message': f'Failed to create directory'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def get_content(payload: RegisterPayload) -> Dict[str, str]:
    uid = register_request(payload)
    ret = create_directory(uid)

    if not ret:
        raise FailedCreateDirectory()

    message = 'Register Successful'

    content = {
        'message': message
    }

    return content


def register_request(payload: RegisterPayload) -> str:
    api_key = os.environ['API_KEY']
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"

    auth_payload = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=auth_payload)
    if response.status_code != 200:
        raise InvalidRegisterError()

    return response.json().get("localId")


def create_directory(uid: str) -> bool:
    try:
        client = storage.Client()
        bucket = client.get_bucket(os.environ["BUCKET"])
        path = f'documents/{uid}/.keep'
        blob = bucket.blob(path)

        if not blob.exists():
            blob.upload_from_string('', content_type='text/plain')

        return True

    except Exception:
        raise FailedCreateDirectory()
