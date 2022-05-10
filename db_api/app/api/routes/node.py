from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.node import NodeVersion
from db import crud
from db.database import get_db


router = APIRouter(
    prefix="/node",
    tags=["Node"],
)


#
# READ
#


def get_node_version(uuid: UUID, db: Session = Depends(get_db)):
    return crud.node.read_by_uuid(uuid=uuid, db=db)


helpers.api_route_read(router, get_node_version, NodeVersion, path="/{uuid}/version")
