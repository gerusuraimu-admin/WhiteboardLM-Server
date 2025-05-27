import os
import requests
from typing import Dict
import vertexai
from vertexai import rag
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


class FailedCreateCorpus(Exception):
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
    create_corpus(uid)
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


def create_corpus(uid: str) -> None:
    try:
        project = os.environ['PROJECT_ID']
        location = 'us-central1'
        display_name = uid
        model = 'text-multilingual-embedding-002'

        vertexai.init(project=project, location=location)

        rag_embedding_model_config = rag.RagEmbeddingModelConfig(
            rag.VertexPredictionEndpoint(
                publisher_model=f'projects/{project}/locations/{location}/publishers/google/models/{model}'
            )
        )

        rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag_embedding_model_config
            )
        )

    except Exception:
        raise FailedCreateCorpus()
