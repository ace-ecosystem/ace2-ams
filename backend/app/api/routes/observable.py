from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from typing import List, Union
from uuid import UUID

from api.models.observable import (
    ObservableCreate,
    ObservableCreateWithAlert,
    ObservableRead,
    ObservableUpdate,
)
from api.routes import helpers
from api.routes.node import create_node, update_node
from core.auth import validate_access_token
from db import crud
from db.database import get_db
from db.schemas.observable import Observable, ObservableHistory
from db.schemas.observable_type import ObservableType


router = APIRouter(
    prefix="/observable",
    tags=["Observable"],
)


#
# CREATE
#


def _create_observable(observable: Union[ObservableCreate, ObservableCreateWithAlert], db: Session) -> Observable:
    # First check if this observable already exists
    existing_observable = crud.read_observable(type=observable.type, value=observable.value, db=db)
    if existing_observable:
        return existing_observable

    new_observable: Observable = create_node(
        node_create=observable,
        db_node_type=Observable,
        db=db,
        exclude={"node_tree"},
    )

    # Get the observable type from the database to associate with the new observable
    new_observable.type = crud.read_by_value(observable.type, db_table=ObservableType, db=db)

    # Set the redirection observable if one was given
    if observable.redirection_uuid:
        new_observable.redirection = crud.read(
            uuid=observable.redirection_uuid,
            db_table=Observable,
            db=db,
        )

    return new_observable


def create_observables(
    observables: List[ObservableCreate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    username: str = Depends(validate_access_token),
):
    # NOTE: There are multiple crud.commit(db) statements to avoid the possibility of
    # getting an IntegrityError when trying to read the observable from the Node table. This
    # can happen due to autoflush in the case of trying to create observables with the same UUID.

    # Add each observable to the database
    for observable in observables:
        new_observable: Observable = _create_observable(observable=observable, db=db)
        db.add(new_observable)
        observable.uuid = new_observable.uuid

        # Add an entry to the history table
        crud.record_create_history(
            history_table=ObservableHistory,
            action_by=username,
            record_read_model=ObservableRead,
            record_table=Observable,
            record_uuid=new_observable.uuid,
            db=db,
        )

    crud.commit(db)

    # Then link them to a Node Tree
    for observable in observables:
        crud.create_node_tree_leaf(
            node_metadata=observable.node_tree.node_metadata,
            root_node_uuid=observable.node_tree.root_node_uuid,
            parent_tree_uuid=observable.node_tree.parent_tree_uuid,
            node_uuid=observable.uuid,
            db=db,
        )

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=new_observable.uuid)


helpers.api_route_create(router, create_observables)


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
    username: str = Depends(validate_access_token),
):
    # Update the Node attributes
    db_observable, diffs = update_node(node_update=observable, uuid=uuid, db_table=Observable, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = observable.dict(exclude_unset=True)

    if "context" in update_data:
        diffs.append(crud.create_diff(field="context", old=db_observable.context, new=update_data["context"]))
        db_observable.context = update_data["context"]

    if "expires_on" in update_data:
        diffs.append(crud.create_diff(field="expires_on", old=db_observable.expires_on, new=update_data["expires_on"]))
        db_observable.expires_on = update_data["expires_on"]

    if "for_detection" in update_data:
        diffs.append(
            crud.create_diff(field="for_detection", old=db_observable.for_detection, new=update_data["for_detection"])
        )
        db_observable.for_detection = update_data["for_detection"]

    if "redirection_uuid" in update_data:
        diffs.append(
            crud.create_diff(
                field="redirection_uuid", old=db_observable.redirection_uuid, new=update_data["redirection_uuid"]
            )
        )

        if update_data["redirection_uuid"]:
            db_observable.redirection = crud.read(uuid=update_data["redirection_uuid"], db_table=Observable, db=db)

            # TODO: Figure out why setting the redirection field above does not set the redirection_uuid
            # the same way it does in the create endpoint.
            db_observable.redirection_uuid = update_data["redirection_uuid"]
        else:
            # At this point we want to set the redirection back to None. If there actually is
            # a redirection observable set, then set both observables' redirection_uuid to None.
            if db_observable.redirection:
                db_observable.redirection.redirection_uuid = None
                db_observable.redirection_uuid = None

    if "time" in update_data:
        diffs.append(crud.create_diff(field="time", old=db_observable.time, new=update_data["time"]))
        db_observable.time = update_data["time"]

    if "type" in update_data:
        diffs.append(crud.create_diff(field="type", old=db_observable.type.value, new=update_data["type"]))
        db_observable.type = crud.read_by_value(value=update_data["type"], db_table=ObservableType, db=db)

    if "value" in update_data:
        diffs.append(crud.create_diff(field="value", old=db_observable.value, new=update_data["value"]))
        db_observable.value = update_data["value"]

    crud.commit(db)

    # Add the entries to the history table
    crud.record_update_histories(
        history_table=ObservableHistory,
        action_by=username,
        record_read_model=ObservableRead,
        record_table=Observable,
        record_uuid=db_observable.uuid,
        diffs=diffs,
        db=db,
    )

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=uuid)


helpers.api_route_update(router, update_observable)


#
# DELETE
#


# We currently do not support deleting observables
