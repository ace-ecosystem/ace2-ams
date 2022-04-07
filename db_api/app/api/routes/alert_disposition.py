from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.alert_disposition import (
    AlertDispositionCreate,
    AlertDispositionRead,
    AlertDispositionUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.alert_disposition import AlertDisposition


router = APIRouter(
    prefix="/alert/disposition",
    tags=["Alert Disposition"],
)


#
# CREATE
#


def create_disposition(
    create: AlertDispositionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj: AlertDisposition = crud.create(obj=create, db_table=AlertDisposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=obj.uuid)


helpers.api_route_create(router, create_disposition)


#
# READ
#


def get_all_dispositions(db: Session = Depends(get_db)):
    return paginate(db, select(AlertDisposition).order_by(AlertDisposition.rank))


def get_disposition(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AlertDisposition, db=db)


helpers.api_route_read_all(router, get_all_dispositions, AlertDispositionRead)
helpers.api_route_read(router, get_disposition, AlertDispositionRead)


#
# UPDATE
#


def update_disposition(
    uuid: UUID,
    disposition: AlertDispositionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=disposition, db_table=AlertDisposition, db=db)

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=uuid)


helpers.api_route_update(router, update_disposition)


#
# DELETE
#


def delete_disposition(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AlertDisposition, db=db)


helpers.api_route_delete(router, delete_disposition)
