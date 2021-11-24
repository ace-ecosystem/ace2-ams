from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.observable import (
    ObservableCreate,
    ObservableRead,
    ObservableUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


router = APIRouter(
    prefix="/observable",
    tags=["Observable"],
)


#
# CREATE
#


def create_observable(
    observable: ObservableCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new observable using the data from the request
    new_observable = Observable(**observable.dict())

    # Get the observable type from the database to associate with the new observable
    new_observable.type = crud.read_by_value(observable.type, db_table=ObservableType, db=db)

    # Save the new observable to the database
    db.add(new_observable)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=new_observable.uuid)


helpers.api_route_create(router, create_observable)


#
# READ
#


def get_all_observables(db: Session = Depends(get_db)):
    return paginate(db, select(Observable))


def get_observable(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Observable, db=db)


helpers.api_route_read_all(router, get_all_observables, ObservableRead)
helpers.api_route_read(router, get_observable, ObservableRead)


#
# UPDATE
#


def update_observable(
    uuid: UUID,
    observable: ObservableUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Read the current observable from the database
    db_observable: Observable = crud.read(uuid=uuid, db_table=Observable, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = observable.dict(exclude_unset=True)

    if "expires_on" in update_data:
        db_observable.expires_on = update_data["expires_on"]

    if "for_detection" in update_data:
        db_observable.for_detection = update_data["for_detection"]

    if "type" in update_data:
        db_observable.type = crud.read_by_value(value=update_data["type"], db_table=ObservableType, db=db)

    if "value" in update_data:
        db_observable.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=uuid)


helpers.api_route_update(router, update_observable)


#
# DELETE
#


def delete_observable(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=Observable, db=db)


helpers.api_route_delete(router, delete_observable)
