from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.threat_actor import ThreatActorRead


router = APIRouter(
    prefix="/threat_actor",
    tags=["Threat Actor"],
)


#
# READ
#


def get_all_threat_actors(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/threat_actor/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_threat_actors, ThreatActorRead)
