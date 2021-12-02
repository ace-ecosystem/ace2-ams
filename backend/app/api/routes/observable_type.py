from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.observable_type import (
    ObservableTypeCreate,
    ObservableTypeRead,
    ObservableTypeUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.observable_type import ObservableType


router = APIRouter(
    prefix="/observable/type",
    tags=["Observable Type"],
)


#
# CREATE
#


def create_observable_type(
    observable_type: ObservableTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=observable_type, db_table=ObservableType, db=db)

    response.headers["Content-Location"] = request.url_for("get_observable_type", uuid=uuid)


helpers.api_route_create(router, create_observable_type)


#
# READ
#


def get_all_observable_types(db: Session = Depends(get_db)):
    return paginate(db, select(ObservableType))


def get_observable_type(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=ObservableType, db=db)


helpers.api_route_read_all(router, get_all_observable_types, ObservableTypeRead)
helpers.api_route_read(router, get_observable_type, ObservableTypeRead)


#
# UPDATE
#


def update_observable_type(
    uuid: UUID,
    observable_type: ObservableTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=observable_type, db_table=ObservableType, db=db)

    response.headers["Content-Location"] = request.url_for("get_observable_type", uuid=uuid)


helpers.api_route_update(router, update_observable_type)


#
# DELETE
#


def delete_observable_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=ObservableType, db=db)


helpers.api_route_delete(router, delete_observable_type)
