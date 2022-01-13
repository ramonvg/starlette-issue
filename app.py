from requests.exceptions import Timeout
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from asyncio import sleep
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import requests
from starlette.middleware import Middleware


async def get_timeout(request):
    await requests.get("http://localhost:8000/sleep", timeout=1)


async def get_sleep(request):
    await sleep(3)
    return JSONResponse(
        {"detail": "whatever"},
        status_code=200,
    )


class DummyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        return await call_next(request)


async def handle_timeout(request, exc):
    return JSONResponse(
        {"detail": "A timeout happened"},
        status_code=408,
    )


exception_handlers = {
    Timeout: handle_timeout,
}


app = Starlette(
    debug=True,
    routes=[Route("/timeout", get_timeout), Route("/sleep", get_sleep)],
    middleware=[Middleware(DummyMiddleware), Middleware(DummyMiddleware)],
    exception_handlers=exception_handlers,
)
