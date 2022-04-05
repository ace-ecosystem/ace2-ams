import requests

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from api_models.event_risk_level import EventRiskLevelRead
from api.routes import helpers
from core.config import get_settings


router = APIRouter(
    prefix="/event/risk_level",
    tags=["Event Risk Level"],
)


#
# READ
#


def get_all_event_risk_levels(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    try:
        result = requests.get(
            f"{get_settings().database_api_url}/event/risk_level/?limit={limit}&offset={offset}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


helpers.api_route_read_all(router, get_all_event_risk_levels, EventRiskLevelRead)
