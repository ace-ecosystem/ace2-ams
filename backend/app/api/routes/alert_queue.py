from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.alert_queue import AlertQueueCreate, AlertQueueRead, AlertQueueUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.alert_queue import AlertQueue


router = APIRouter(
    prefix="/alert/queue",
    tags=["Alert Queue"],
)


#
# CREATE
#


def create_alert_queue(
    alert_queue: AlertQueueCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=alert_queue, db_table=AlertQueue, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_queue", uuid=uuid)


helpers.api_route_create(router, create_alert_queue)


#
# READ
#


def get_all_alert_queues(db: Session = Depends(get_db)):
    return paginate(db, select(AlertQueue).order_by(AlertQueue.value))


def get_alert_queue(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AlertQueue, db=db)


helpers.api_route_read_all(router, get_all_alert_queues, AlertQueueRead)
helpers.api_route_read(router, get_alert_queue, AlertQueueRead)


#
# UPDATE
#


def update_alert_queue(
    uuid: UUID,
    alert_queue: AlertQueueUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=alert_queue, db_table=AlertQueue, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_queue", uuid=uuid)


helpers.api_route_update(router, update_alert_queue)


#
# DELETE
#


def delete_alert_queue(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AlertQueue, db=db)


helpers.api_route_delete(router, delete_alert_queue)
