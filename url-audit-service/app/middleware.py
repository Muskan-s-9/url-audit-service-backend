from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response


def add_request_id_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestIDMiddleware)
