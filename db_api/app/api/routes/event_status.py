from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_status import (
    EventStatusCreate,
    EventStatusRead,
    EventStatusUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_status import EventStatus
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/event/status",
    tags=["Event Status"],
)


#
# CREATE
#


def create_event_status(
    create: EventStatusCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.event_status.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=obj.uuid)


helpers.api_route_create(router, create_event_status)


#
# READ
#


def get_all_event_statuss(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventStatus).order_by(EventStatus.value))


def get_event_status(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_status.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_statuss, EventStatusRead)
helpers.api_route_read(router, get_event_status, EventStatusRead)


#
# UPDATE
#


def update_event_status(
    uuid: UUID,
    event_status: EventStatusUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_status, db_table=EventStatus, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event status {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=uuid)


helpers.api_route_update(router, update_event_status)


#
# DELETE
#


def delete_event_status(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventStatus, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event status {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_event_status)
