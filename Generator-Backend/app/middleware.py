from fastapi import Request
from starlette.middleware.cors import CORSMiddleware


def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def add_request_id(request: Request, call_next):
    response = await call_next(request)
    return response