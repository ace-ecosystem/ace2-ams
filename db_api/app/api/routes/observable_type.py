from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.observable_type import (
    ObservableTypeCreate,
    ObservableTypeRead,
    ObservableTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.observable_type import ObservableType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/observable/type",
    tags=["Observable Observable Type"],
)


#
# CREATE
#


def create_type(
    create: ObservableTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.observable_type.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_type", uuid=obj.uuid)


helpers.api_route_create(router, create_type)


#
# READ
#


def get_all_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(ObservableType).order_by(ObservableType.value))


def get_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.observable_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_types, ObservableTypeRead)
helpers.api_route_read(router, get_type, ObservableTypeRead)


#
# UPDATE
#


def update_type(
    uuid: UUID,
    type: ObservableTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=type, db_table=ObservableType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update observable type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_type", uuid=uuid)


helpers.api_route_update(router, update_type)


#
# DELETE
#


def delete_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=ObservableType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete observable type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_type)
