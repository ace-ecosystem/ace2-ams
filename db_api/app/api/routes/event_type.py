from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_type import (
    EventTypeCreate,
    EventTypeRead,
    EventTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_type import EventType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/event/type",
    tags=["Event Type"],
)


#
# CREATE
#


def create_event_type(
    create: EventTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.event_type.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_type", uuid=obj.uuid)


helpers.api_route_create(router, create_event_type)


#
# READ
#


def get_all_event_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventType).order_by(EventType.value))


def get_event_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_types, EventTypeRead)
helpers.api_route_read(router, get_event_type, EventTypeRead)


#
# UPDATE
#


def update_event_type(
    uuid: UUID,
    event_type: EventTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_type, db_table=EventType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_event_type", uuid=uuid)


helpers.api_route_update(router, update_event_type)


#
# DELETE
#


def delete_event_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_event_type)
