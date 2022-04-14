from fastapi import APIRouter, status
from uuid import UUID

from api import db_api
from api.routes import helpers


router = APIRouter(
    prefix="/node/tree",
    tags=["Node Tree"],
)


#
# READ
#


def get_node_tree_nodes(node_type: str, root_node_uuids: list[UUID]):
    return db_api.post(
        path=f"/node/tree/{node_type}", payload=[str(u) for u in root_node_uuids], expected_status=status.HTTP_200_OK
    )


helpers.api_route_read(router, get_node_tree_nodes, list[dict], methods=["POST"], path="/{node_type}")
