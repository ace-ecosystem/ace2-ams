from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api_models.queue import QueueCreate, QueueRead, QueueUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.queue import Queue


router = APIRouter(
    prefix="/queue",
    tags=["Queue"],
)


#
# CREATE
#


def create_queue(
    create: QueueCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj: Queue = crud.create(obj=create, db_table=Queue, db=db)

    response.headers["Content-Location"] = request.url_for("get_queue", uuid=obj.uuid)


helpers.api_route_create(router, create_queue)


#
# READ
#


def get_all_queues(db: Session = Depends(get_db)):
    return paginate(db, select(Queue).order_by(Queue.value))


def get_queue(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Queue, db=db)


helpers.api_route_read_all(router, get_all_queues, QueueRead)
helpers.api_route_read(router, get_queue, QueueRead)


#
# UPDATE
#


def update_queue(
    uuid: UUID,
    queue: QueueUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=queue, db_table=Queue, db=db)

    response.headers["Content-Location"] = request.url_for("get_queue", uuid=uuid)


helpers.api_route_update(router, update_queue)


#
# DELETE
#


def delete_queue(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=Queue, db=db)


helpers.api_route_delete(router, delete_queue)
