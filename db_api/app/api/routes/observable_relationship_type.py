from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.observable_relationship_type import (
    ObservableRelationshipTypeCreate,
    ObservableRelationshipTypeRead,
    ObservableRelationshipTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.observable_relationship_type import ObservableRelationshipType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/node/relationship/type",
    tags=["Node Relationship Type"],
)


#
# CREATE
#


def create_observable_relationship_type(
    create: ObservableRelationshipTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.observable_relationship_type.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_observable_relationship_type", uuid=obj.uuid)


helpers.api_route_create(router, create_observable_relationship_type)


#
# READ
#


def get_all_observable_relationship_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.observable_relationship_type.build_read_all_query())


def get_observable_relationship_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.observable_relationship_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_observable_relationship_types, ObservableRelationshipTypeRead)
helpers.api_route_read(router, get_observable_relationship_type, ObservableRelationshipTypeRead)


#
# UPDATE
#


def update_observable_relationship_type(
    uuid: UUID,
    observable_relationship: ObservableRelationshipTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=observable_relationship, db_table=ObservableRelationshipType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node relationship type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_observable_relationship_type", uuid=uuid)


helpers.api_route_update(router, update_observable_relationship_type)


#
# DELETE
#


def delete_observable_relationship_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=ObservableRelationshipType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node relationship type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_observable_relationship_type)
