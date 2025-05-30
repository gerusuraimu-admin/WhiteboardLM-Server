from typing import Dict
from utils.Payload import AuthPayload, Response
from utils.Session import Session, InvalidAuthError, SessionTimeOutError

"""
AuthPayload:
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
    - Auth Successful ... 正規ユーザーによるリクエストとして扱った
    - Invalid Auth ... 正規ユーザーによるリクエストとして扱えなかった
    - その他例外
"""


def handle_auth(payload: AuthPayload, session: Session) -> Response:
    try:
        return Response(status_code=200, content=get_content(payload, session))

    except InvalidAuthError as e:
        return Response(status_code=401, content={'message': f'Invalid Auth ... {e}'})

    except SessionTimeOutError:
        return Response(status_code=401, content={'message': 'Session Timed Out'})

    except Exception as e:
        return Response(status_code=500, content={'message': str(e)})


def get_content(payload: AuthPayload, session: Session) -> Dict[str, str]:
    session_id = session.auth(payload.uid, payload.session_id)
    message = 'Auth Successful'

    content = {
        'uid': payload.uid,
        'session_id': session_id,
        'message': message
    }

    return content
