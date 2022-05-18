from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_vector import (
    EventVectorCreate,
    EventVectorRead,
    EventVectorUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_vector import EventVector
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/event/vector",
    tags=["Event Vector"],
)


#
# CREATE
#


def create_event_vector(
    create: EventVectorCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.event_vector.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_vector", uuid=obj.uuid)


helpers.api_route_create(router, create_event_vector)


#
# READ
#


def get_all_event_vectors(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventVector).order_by(EventVector.value))


def get_event_vector(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_vector.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_vectors, EventVectorRead)
helpers.api_route_read(router, get_event_vector, EventVectorRead)


#
# UPDATE
#


def update_event_vector(
    uuid: UUID,
    event_vector: EventVectorUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_vector, db_table=EventVector, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event vector {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_vector", uuid=uuid)


helpers.api_route_update(router, update_event_vector)


#
# DELETE
#


def delete_event_vector(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventVector, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event vector {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_event_vector)
