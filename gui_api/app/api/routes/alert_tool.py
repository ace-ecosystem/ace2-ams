import requests

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from api_models.alert_tool import AlertToolRead
from api.routes import helpers
from core.config import get_settings


router = APIRouter(
    prefix="/alert/tool",
    tags=["Alert Tool"],
)


#
# READ
#


def get_all_tools(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    try:
        result = requests.get(
            f"{get_settings().database_api_url}/alert/tool/?limit={limit}&offset={offset}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


helpers.api_route_read_all(router, get_all_tools, AlertToolRead)
