from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api_models.node_relationship_type import (
    NodeRelationshipTypeCreate,
    NodeRelationshipTypeRead,
    NodeRelationshipTypeUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_relationship_type import NodeRelationshipType


router = APIRouter(
    prefix="/node/relationship/type",
    tags=["Node Relationship Type"],
)


#
# CREATE
#


def create_node_relationship_type(
    create: NodeRelationshipTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj: NodeRelationshipType = crud.create(obj=create, db_table=NodeRelationshipType, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_relationship_type", uuid=obj.uuid)


helpers.api_route_create(router, create_node_relationship_type)


#
# READ
#


def get_all_node_relationship_types(db: Session = Depends(get_db)):
    return paginate(db, select(NodeRelationshipType).order_by(NodeRelationshipType.value))


def get_node_relationship_type(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeRelationshipType, db=db)


helpers.api_route_read_all(router, get_all_node_relationship_types, NodeRelationshipTypeRead)
helpers.api_route_read(router, get_node_relationship_type, NodeRelationshipTypeRead)


#
# UPDATE
#


def update_node_relationship_type(
    uuid: UUID,
    node_relationship: NodeRelationshipTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=node_relationship, db_table=NodeRelationshipType, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_relationship_type", uuid=uuid)


helpers.api_route_update(router, update_node_relationship_type)


#
# DELETE
#


def delete_node_relationship_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeRelationshipType, db=db)


helpers.api_route_delete(router, delete_node_relationship_type)
