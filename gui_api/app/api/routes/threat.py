import json

from fastapi import APIRouter, Query, Request, Response
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.threat import ThreatCreate, ThreatRead, ThreatUpdate


router = APIRouter(
    prefix="/threat",
    tags=["Threat"],
)


#
# CREATE
#


def create_threat(
    threat: ThreatCreate,
    request: Request,
    response: Response,
):
    result = db_api.post(path="/threat/", payload=json.loads(threat.json()))

    response.headers["Content-Location"] = request.url_for("get_threat", uuid=result["uuid"])


helpers.api_route_create(router, create_threat)


#
# READ
#


def get_threat(uuid: UUID):
    return db_api.get(path=f"/threat/{uuid}")


def get_all_threats(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/threat/?limit={limit}&offset={offset}")


helpers.api_route_read(router, get_threat, ThreatRead)
helpers.api_route_read_all(router, get_all_threats, ThreatRead)


#
# UPDATE
#


def update_threat(
    uuid: UUID,
    threat: ThreatUpdate,
    request: Request,
    response: Response,
):
    db_api.patch(
        path=f"/threat/{uuid}",
        payload=json.loads(threat.json(exclude_unset=True)),
    )

    response.headers["Content-Location"] = request.url_for("get_threat", uuid=uuid)


helpers.api_route_update(router, update_threat)
