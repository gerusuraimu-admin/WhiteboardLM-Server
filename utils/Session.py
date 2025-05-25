from time import time
from typing import Dict
from hashlib import sha512
from threading import Lock

"""
プロダクトの本番環境でこんなセッション使ったら死ぬけど、今はまぁええやろ。
"""


class InvalidAuthError(Exception):
    pass


class Session:
    _lock: Lock = Lock()
    _instance: "Session" = None

    def __init__(self) -> None:
        self.session: Dict[str, float] = dict()

    def __new__(cls, *args, **kwargs) -> "Session":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def auth(self, uid: str, session_id: str) -> str:
        if self.session.get(uid) is None:
            raise InvalidAuthError()

        if self.__get_session_id(uid) != session_id:
            raise InvalidAuthError()

        if 300 <= time() - self.session.get(uid):
            with self._lock:
                del self.session[uid]
            raise InvalidAuthError()

        return self.login(uid)

    def login(self, uid: str) -> str:
        with self._lock:
            self.session[uid] = time()
        return self.__get_session_id(uid)

    def logout(self, uid: str, session_id: str) -> bool:
        if self.auth(uid, session_id):
            with self._lock:
                del self.session[uid]
            return True
        else:
            return False

    def __get_session_id(self, uid: str) -> str:
        get_time: float = self.session.get(uid)
        script = f'{uid}{get_time}'
        return sha512(script.encode()).hexdigest()
