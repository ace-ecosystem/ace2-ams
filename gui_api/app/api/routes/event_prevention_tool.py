from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.event_prevention_tool import EventPreventionToolRead


router = APIRouter(
    prefix="/event/prevention_tool",
    tags=["Event Prevention Tool"],
)


#
# READ
#


def get_all_event_prevention_tools(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/event/prevention_tool/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_event_prevention_tools, EventPreventionToolRead)
