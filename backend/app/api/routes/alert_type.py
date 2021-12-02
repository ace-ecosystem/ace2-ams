from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.alert_type import AlertTypeCreate, AlertTypeRead, AlertTypeUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.alert_type import AlertType


router = APIRouter(
    prefix="/alert/type",
    tags=["Alert Type"],
)


#
# CREATE
#


def create_alert_type(
    alert_type: AlertTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=alert_type, db_table=AlertType, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_type", uuid=uuid)


helpers.api_route_create(router, create_alert_type)


#
# READ
#


def get_all_alert_types(db: Session = Depends(get_db)):
    return paginate(db, select(AlertType))


def get_alert_type(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AlertType, db=db)


helpers.api_route_read_all(router, get_all_alert_types, AlertTypeRead)
helpers.api_route_read(router, get_alert_type, AlertTypeRead)


#
# UPDATE
#


def update_alert_type(
    uuid: UUID,
    alert_type: AlertTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=alert_type, db_table=AlertType, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_type", uuid=uuid)


helpers.api_route_update(router, update_alert_type)


#
# DELETE
#


def delete_alert_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AlertType, db=db)


helpers.api_route_delete(router, delete_alert_type)
