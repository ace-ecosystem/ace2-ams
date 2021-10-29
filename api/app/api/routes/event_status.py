from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.event_status import (
    EventStatusCreate,
    EventStatusRead,
    EventStatusUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event_status import EventStatus


router = APIRouter(
    prefix="/event/status",
    tags=["Event Status"],
)


#
# CREATE
#


def create_event_status(
    event_status: EventStatusCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=event_status, db_table=EventStatus, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=uuid)


helpers.api_route_create(router, create_event_status)


#
# READ
#


def get_all_event_statuses(db: Session = Depends(get_db)):
    return crud.read_all(db_table=EventStatus, db=db)


def get_event_status(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventStatus, db=db)


helpers.api_route_read_all(router, get_all_event_statuses, List[EventStatusRead])
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
    crud.update(uuid=uuid, obj=event_status, db_table=EventStatus, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=uuid)


helpers.api_route_update(router, update_event_status)


#
# DELETE
#


def delete_event_status(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventStatus, db=db)


helpers.api_route_delete(router, delete_event_status)
