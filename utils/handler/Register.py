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


def handle_register(payload: RegisterPayload) -> Response:
    pass
