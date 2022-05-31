import json

from fastapi import APIRouter, Request, Response
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.node_detection_point import NodeDetectionPointCreate, NodeDetectionPointRead


router = APIRouter(
    prefix="/node/detection_point",
    tags=["Node Detection Point"],
)


#
# CREATE
#


def create_node_detection_points(
    node_detection_points: list[NodeDetectionPointCreate],
    request: Request,
    response: Response,
):
    result = db_api.post(path="/node/detection_point", payload=[json.loads(d.json()) for d in node_detection_points])

    response.headers["Content-Location"] = request.url_for("get_node_detection_point", uuid=result["uuid"])


helpers.api_route_create(router, create_node_detection_points)


#
# READ
#


def get_node_detection_point(uuid: UUID):
    return db_api.get(path=f"/node/detection_point/{uuid}")


helpers.api_route_read(router, get_node_detection_point, NodeDetectionPointRead)
