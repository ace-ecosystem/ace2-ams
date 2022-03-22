from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.node_relationship import (
    NodeRelationshipCreate,
    NodeRelationshipRead,
    NodeRelationshipUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_relationship import NodeRelationship


router = APIRouter(
    prefix="/node/relationship",
    tags=["Node Relationship"],
)


#
# CREATE
#


def create_node_relationship(
    create: NodeRelationshipCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj: NodeRelationship = crud.create(obj=create, db_table=NodeRelationship, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_relationship", uuid=obj.uuid)


helpers.api_route_create(router, create_node_relationship)


#
# READ
#


def get_all_node_relationships(db: Session = Depends(get_db)):
    return paginate(db, select(NodeRelationship).order_by(NodeRelationship.value))


def get_node_relationship(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeRelationship, db=db)


helpers.api_route_read_all(router, get_all_node_relationships, NodeRelationshipRead)
helpers.api_route_read(router, get_node_relationship, NodeRelationshipRead)


#
# UPDATE
#


def update_node_relationship(
    uuid: UUID,
    node_relationship: NodeRelationshipUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=node_relationship, db_table=NodeRelationship, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_relationship", uuid=uuid)


helpers.api_route_update(router, update_node_relationship)


#
# DELETE
#


def delete_node_relationship(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeRelationship, db=db)


helpers.api_route_delete(router, delete_node_relationship)
