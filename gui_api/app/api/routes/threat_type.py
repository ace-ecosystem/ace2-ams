from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.threat_type import ThreatTypeRead


router = APIRouter(
    prefix="/node/threat/type",
    tags=["Node Threat Type"],
)


#
# READ
#


def get_all_threat_types(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/node/threat/type/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_threat_types, ThreatTypeRead)
