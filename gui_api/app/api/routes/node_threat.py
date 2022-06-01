import json

from fastapi import APIRouter, Query, Request, Response
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.node_threat import NodeThreatCreate, NodeThreatRead, NodeThreatUpdate


router = APIRouter(
    prefix="/node/threat",
    tags=["Node Threat"],
)


#
# CREATE
#


def create_node_threat(
    node_threat: NodeThreatCreate,
    request: Request,
    response: Response,
):
    result = db_api.post(path="/node/threat/", payload=json.loads(node_threat.json()))

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=result["uuid"])


helpers.api_route_create(router, create_node_threat)


#
# READ
#


def get_node_threat(uuid: UUID):
    return db_api.get(path=f"/node/threat/{uuid}")


def get_all_node_threats(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/node/threat/?limit={limit}&offset={offset}")


helpers.api_route_read(router, get_node_threat, NodeThreatRead)
helpers.api_route_read_all(router, get_all_node_threats, NodeThreatRead)


#
# UPDATE
#


def update_node_threat(
    uuid: UUID,
    node_threat: NodeThreatUpdate,
    request: Request,
    response: Response,
):
    db_api.patch(
        path=f"/node/threat/{uuid}",
        payload=json.loads(node_threat.json(exclude_unset=True)),
    )

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=uuid)


helpers.api_route_update(router, update_node_threat)
