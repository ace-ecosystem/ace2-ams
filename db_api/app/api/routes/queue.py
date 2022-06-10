from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.queue import QueueCreate, QueueRead, QueueUpdate
from db import crud
from db.database import get_db
from db.schemas.queue import Queue
from exceptions.db import UuidNotFoundInDatabase


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
    obj = crud.queue.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_queue", uuid=obj.uuid)


helpers.api_route_create(router, create_queue)


#
# READ
#


def get_all_queues(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.queue.build_read_all_query())


def get_queue(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.queue.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=queue, db_table=Queue, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update queue {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_queue", uuid=uuid)


helpers.api_route_update(router, update_queue)


#
# DELETE
#


def delete_queue(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=Queue, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete queue {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_queue)
