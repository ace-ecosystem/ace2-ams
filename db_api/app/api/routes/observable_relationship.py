from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.observable_relationship import ObservableRelationshipCreate, ObservableRelationshipRead
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/node/relationship",
    tags=["Node Relationship"],
)


#
# CREATE
#


def create_observable_relationship(
    create: ObservableRelationshipCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.observable_relationship.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_observable_relationship", uuid=obj.uuid)


helpers.api_route_create(router, create_observable_relationship)


#
# READ
#


def get_observable_relationship(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.observable_relationship.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read(router, get_observable_relationship, ObservableRelationshipRead)


#
# DELETE
#


def delete_observable_relationship(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.observable_relationship.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_observable_relationship)
