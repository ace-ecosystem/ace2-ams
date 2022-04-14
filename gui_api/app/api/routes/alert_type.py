from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.alert_type import AlertTypeRead


router = APIRouter(
    prefix="/alert/type",
    tags=["Alert Type"],
)


#
# READ
#


def get_all_alert_types(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/alert/type/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_alert_types, AlertTypeRead)
