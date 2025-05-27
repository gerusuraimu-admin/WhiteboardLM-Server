from typing import Dict
from utils.Payload import LogoutPayload, Response
from utils.Session import Session, InvalidAuthError

"""
LogoutPayload:
    uid: str
    session_id: str

Response:
    status_code: int
    content: Dict[str, Any]

content = {
    'uid': uid,
    'session_id': session_id,
    'message': message
}

message:
    - Logout Successful ... 正規のユーザーからのログアウトリクエストが成功した
    - Invalid Auth ... 正規ユーザーによるリクエストとして扱えなかった
    - その他例外
"""


def handle_logout(payload: LogoutPayload) -> Response:
    try:
        return Response(status_code=200, content=get_content(payload))

    except InvalidAuthError:
        return Response(status_code=401, content={'message': 'Invalid Auth'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def get_content(payload: LogoutPayload) -> Dict[str, str]:
    session = Session()
    ret = session.logout(payload.uid, payload.session_id)

    if not ret:
        raise InvalidAuthError

    message = 'Logout Successful'

    content = {
        'uid': payload.uid,
        'session_id': payload.session_id,
        'message': message
    }

    return content
