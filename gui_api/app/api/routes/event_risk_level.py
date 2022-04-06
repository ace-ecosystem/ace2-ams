from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.event_risk_level import EventRiskLevelRead


router = APIRouter(
    prefix="/event/risk_level",
    tags=["Event Risk Level"],
)


#
# READ
#


def get_all_event_risk_levels(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/event/risk_level/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_event_risk_levels, EventRiskLevelRead)
