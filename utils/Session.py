from time import time
from typing import Dict
from hashlib import sha512
from threading import Lock

"""
プロダクトの本番環境でこんなセッション使ったら死ぬけど、今はまぁええやろ。
"""


class InvalidAuthError(Exception):
    pass


class SessionTimeOutError(Exception):
    pass


class Session:
    _lock: Lock = Lock()
    _instance: "Session" = None

    def __init__(self) -> None:
        self.session: Dict[str, float] = dict()
        self.token: Dict[str, str] = dict()

    def __new__(cls, *args, **kwargs) -> "Session":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def auth(self, uid: str, session_id: str) -> str:
        if self.__get_session_id(uid) != session_id:
            raise InvalidAuthError()

        if 300 <= time() - self.session.get(uid):
            with self._lock:
                del self.session[uid]
            raise SessionTimeOutError()

        token = self.token.get(uid)

        return self.login(uid, token)

    def login(self, uid: str, token: str) -> str:
        with self._lock:
            self.session[uid] = time()
            self.token[uid] = token
        return self.__get_session_id(uid)

    def logout(self, uid: str, session_id: str) -> bool:
        ret = False

        try:
            self.auth(uid, session_id)

        except InvalidAuthError:
            pass

        except Exception:
            raise InvalidAuthError()

        else:
            ret = True

        finally:
            with self._lock:
                if uid in self.session:
                    del self.session[uid]
                if uid in self.token:
                    del self.token[uid]

        return ret

    def __get_session_id(self, uid: str) -> str:
        get_time: float = self.session.get(uid, 0)
        get_token: str = self.token.get(uid, '')
        script = f'{uid}{get_time}{get_token}'
        return sha512(script.encode()).hexdigest()
