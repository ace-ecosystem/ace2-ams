from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.event_severity import EventSeverityRead


router = APIRouter(
    prefix="/event/severity",
    tags=["Event Severity"],
)


#
# READ
#


def get_all_event_severities(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/event/severity/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_event_severities, EventSeverityRead)
