from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.node_relationship import NodeRelationshipCreate, NodeRelationshipRead
from db import crud
from db.database import get_db
from db.schemas.node import Node
from db.schemas.node_relationship import NodeRelationship
from db.schemas.node_relationship_type import NodeRelationshipType
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


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
    obj = crud.node_relationship.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_relationship", uuid=obj.uuid)


helpers.api_route_create(router, create_node_relationship)


#
# READ
#


def get_node_relationship(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_relationship.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read(router, get_node_relationship, NodeRelationshipRead)


#
# DELETE
#


def delete_node_relationship(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.node_relationship.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_relationship)
