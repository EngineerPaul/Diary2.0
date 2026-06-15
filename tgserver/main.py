import uuid

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from api.routers import main_router
from dependencies import set_session, close_session
from utils.logging_config import setup_logging
from utils.request_context import REQUEST_ID_HEADER, set_request_id

setup_logging()

app = FastAPI()
app.include_router(main_router)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware для добавления request_id в запрос и ответ"""

    async def dispatch(self, request, call_next):
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        set_request_id(request_id)
        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            set_request_id(None)


app.add_middleware(RequestIdMiddleware)


@app.on_event("startup")
async def startup_event():
    await set_session()


@app.on_event("shutdown")
async def shutdown_event():
    await close_session()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')
