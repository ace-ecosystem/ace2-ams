from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.node_threat_type import (
    NodeThreatTypeCreate,
    NodeThreatTypeRead,
    NodeThreatTypeUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_threat_type import NodeThreatType


router = APIRouter(
    prefix="/node/threat/type",
    tags=["Node Threat Type"],
)


#
# CREATE
#


def create_node_threat_type(
    node_threat_type: NodeThreatTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=node_threat_type, db_table=NodeThreatType, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=uuid)


helpers.api_route_create(router, create_node_threat_type)


#
# READ
#


def get_all_node_threat_types(db: Session = Depends(get_db)):
    return paginate(db, select(NodeThreatType).order_by(NodeThreatType.value))


def get_node_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeThreatType, db=db)


helpers.api_route_read_all(router, get_all_node_threat_types, NodeThreatTypeRead)
helpers.api_route_read(router, get_node_threat_type, NodeThreatTypeRead)


#
# UPDATE
#


def update_node_threat_type(
    uuid: UUID,
    node_threat_type: NodeThreatTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=node_threat_type, db_table=NodeThreatType, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=uuid)


helpers.api_route_update(router, update_node_threat_type)


#
# DELETE
#


def delete_node_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreatType, db=db)


helpers.api_route_delete(router, delete_node_threat_type)
