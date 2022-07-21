from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.event_vector import EventVectorRead


router = APIRouter(
    prefix="/event/vector",
    tags=["Event Vector"],
)


#
# READ
#


def get_all_event_vectors(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/event/vector/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_event_vectors, EventVectorRead)
