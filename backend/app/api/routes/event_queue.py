from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.event_queue import EventQueueCreate, EventQueueRead, EventQueueUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event_queue import EventQueue


router = APIRouter(
    prefix="/event/queue",
    tags=["Event Queue"],
)


#
# CREATE
#


def create_event_queue(
    event_queue: EventQueueCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=event_queue, db_table=EventQueue, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_queue", uuid=uuid)


helpers.api_route_create(router, create_event_queue)


#
# READ
#


def get_all_event_queues(db: Session = Depends(get_db)):
    return paginate(db, select(EventQueue).order_by(EventQueue.value))


def get_event_queue(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventQueue, db=db)


helpers.api_route_read_all(router, get_all_event_queues, EventQueueRead)
helpers.api_route_read(router, get_event_queue, EventQueueRead)


#
# UPDATE
#


def update_event_queue(
    uuid: UUID,
    event_queue: EventQueueUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=event_queue, db_table=EventQueue, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_queue", uuid=uuid)


helpers.api_route_update(router, update_event_queue)


#
# DELETE
#


def delete_event_queue(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventQueue, db=db)


helpers.api_route_delete(router, delete_event_queue)
