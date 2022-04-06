from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.queue import QueueRead


router = APIRouter(
    prefix="/queue",
    tags=["Queue"],
)


#
# READ
#


def get_all_queues(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/queue/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_queues, QueueRead)
