import functools
from fastapi.responses import JSONResponse
from utils.Payload import Response

"""
意図しないエラーが意図しない箇所で発生し、
ハンドラー内のtry-exceptから漏れても極力その旨を通知できるように
全てのハンドラーをtry-exceptでラップし、500番を返す。
"""


def handle_wrapper(func):
    @functools.wraps(func)
    async def wrapper(payload) -> JSONResponse:
        try:
            response: Response = await func(payload)
            return JSONResponse(**response.__dict__)

        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})

    return wrapper
