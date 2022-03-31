from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from db import crud
from db.database import get_db


router = APIRouter(
    prefix="/node/tree",
    tags=["Node Tree"],
)


#
# READ
#


def get_node_tree_nodes(node_type: str, root_node_uuids: list[UUID], db: Session = Depends(get_db)):
    return crud.read_node_tree_nodes(node_type=node_type, root_node_uuids=root_node_uuids, db=db)


helpers.api_route_read(router, get_node_tree_nodes, list[dict], methods=["POST"], path="/{node_type}")
