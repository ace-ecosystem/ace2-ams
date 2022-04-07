from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.node_threat_type import (
    NodeThreatTypeCreate,
    NodeThreatTypeRead,
    NodeThreatTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.queue import Queue


router = APIRouter(
    prefix="/node/threat/type",
    tags=["Node Threat Type"],
)


#
# CREATE
#


def create_node_threat_type(
    create: NodeThreatTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: NodeThreatType = crud.create(obj=create, db_table=NodeThreatType, db=db, exclude=["queues"])
    obj.queues = queues

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=obj.uuid)


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
    update: NodeThreatTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: NodeThreatType = crud.read(uuid=uuid, db_table=NodeThreatType, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=uuid)


helpers.api_route_update(router, update_node_threat_type)


#
# DELETE
#


def delete_node_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreatType, db=db)


helpers.api_route_delete(router, delete_node_threat_type)
