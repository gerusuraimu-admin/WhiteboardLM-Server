import functools
from fastapi.responses import JSONResponse
from utils.Payload import Response


def handle_wrapper(func):
    @functools.wraps(func)
    async def wrapper(payload):
        try:
            response: Response = await func(payload)
            return JSONResponse(**response.__dict__)

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    return wrapper
