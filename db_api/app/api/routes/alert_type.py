from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.alert_type import AlertTypeCreate, AlertTypeRead, AlertTypeUpdate
from db import crud
from db.database import get_db
from db.schemas.alert_type import AlertType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/alert/type",
    tags=["Alert Type"],
)


#
# CREATE
#


def create_alert_type(
    create: AlertTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.alert_type.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_type", uuid=obj.uuid)


helpers.api_route_create(router, create_alert_type)


#
# READ
#


def get_all_alert_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(AlertType).order_by(AlertType.value))


def get_alert_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.alert_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=alert_type, db_table=AlertType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update alert type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_alert_type", uuid=uuid)


helpers.api_route_update(router, update_alert_type)


#
# DELETE
#


def delete_alert_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=AlertType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete alert type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_alert_type)
