from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.observable_type import ObservableTypeRead


router = APIRouter(
    prefix="/observable/type",
    tags=["Observable Type"],
)


#
# READ
#


def get_all_observable_types(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/observable/type/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_observable_types, ObservableTypeRead)
