"""
Main FastAPI entrypoint
"""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.routes import router as api_router


def get_application():
    """
    Builds and returns the FastAPI application with CORS settings
    """

    _app = FastAPI()

    _app.include_router(api_router, prefix="/api")

    add_pagination(_app)

    return _app


app = get_application()
