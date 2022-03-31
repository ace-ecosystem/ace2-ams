from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api_models.event_status import (
    EventStatusCreate,
    EventStatusRead,
    EventStatusUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.queue import Queue
from db.schemas.event_status import EventStatus


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
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: EventStatus = crud.create(obj=create, db_table=EventStatus, db=db, exclude=["queues"])
    obj.queues = queues

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=obj.uuid)


helpers.api_route_create(router, create_event_status)


#
# READ
#


def get_all_event_statuses(db: Session = Depends(get_db)):
    return paginate(db, select(EventStatus).order_by(EventStatus.value))


def get_event_status(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventStatus, db=db)


helpers.api_route_read_all(router, get_all_event_statuses, EventStatusRead)
helpers.api_route_read(router, get_event_status, EventStatusRead)


#
# UPDATE
#


def update_event_status(
    uuid: UUID,
    update: EventStatusUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: EventStatus = crud.read(uuid=uuid, db_table=EventStatus, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event_status", uuid=uuid)


helpers.api_route_update(router, update_event_status)


#
# DELETE
#


def delete_event_status(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventStatus, db=db)


helpers.api_route_delete(router, delete_event_status)
