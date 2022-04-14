from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.alert_disposition import AlertDispositionRead


router = APIRouter(
    prefix="/alert/disposition",
    tags=["Alert Disposition"],
)


#
# READ
#


def get_all_dispositions(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/alert/disposition/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_dispositions, AlertDispositionRead)
