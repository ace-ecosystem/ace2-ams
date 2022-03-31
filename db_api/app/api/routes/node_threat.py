from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.node_threat import NodeThreatCreate, NodeThreatRead, NodeThreatUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.queue import Queue


router = APIRouter(
    prefix="/node/threat",
    tags=["Node Threat"],
)


#
# CREATE
#


def create_node_threat(
    create: NodeThreatCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    threat_types = crud.read_by_values(values=create.types, db_table=NodeThreatType, db=db)

    # Create the new node threat
    new_threat = NodeThreat(**create.dict(exclude={"queues"}))
    new_threat.queues = queues
    new_threat.types = threat_types

    # Save the new node threat to the database
    db.add(new_threat)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=new_threat.uuid)


helpers.api_route_create(router, create_node_threat)


#
# READ
#


def get_all_node_threats(db: Session = Depends(get_db)):
    return paginate(db, select(NodeThreat).order_by(NodeThreat.value))


def get_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeThreat, db=db)


helpers.api_route_read_all(router, get_all_node_threats, NodeThreatRead)
helpers.api_route_read(router, get_node_threat, NodeThreatRead)


#
# UPDATE
#


def update_node_threat(
    uuid: UUID,
    node_threat: NodeThreatUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Read the current node threat from the database
    db_node_threat: NodeThreat = crud.read(uuid=uuid, db_table=NodeThreat, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = node_threat.dict(exclude_unset=True)

    if "description" in update_data:
        db_node_threat.description = update_data["description"]

    if "queues" in update_data:
        db_node_threat.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_node_threat.value = update_data["value"]

    if "types" in update_data:
        db_node_threat.types = crud.read_by_values(values=update_data["types"], db_table=NodeThreatType, db=db)

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=uuid)


helpers.api_route_update(router, update_node_threat)


#
# DELETE
#


def delete_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreat, db=db)


helpers.api_route_delete(router, delete_node_threat)
