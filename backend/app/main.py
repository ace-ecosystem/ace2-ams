"""
Main FastAPI entrypoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.routes import router as api_router
from core.config import get_settings


def get_application():
    """
    Builds and returns the FastAPI application with CORS settings
    """

    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Location"],
    )

    _app.include_router(api_router, prefix="/api")

    add_pagination(_app)

    return _app


app = get_application()
