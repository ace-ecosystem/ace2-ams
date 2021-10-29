from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID, uuid4

from api.models.observable_instance import ObservableInstanceCreate, ObservableInstanceRead, ObservableInstanceUpdate
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.alert import Alert
from db.schemas.analysis import Analysis
from db.schemas.observable import Observable
from db.schemas.observable_instance import ObservableInstance
from db.schemas.observable_type import ObservableType


router = APIRouter(
    prefix="/observable/instance",
    tags=["Observable Instance"],
)


#
# CREATE
#


def create_observable_instances(
    observable_instances: List[ObservableInstanceCreate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for observable_instance in observable_instances:
        # Create the new observable instance Node using the data from the request
        new_observable_instance: ObservableInstance = create_node(
            node_create=observable_instance,
            db_node_type=ObservableInstance,
            db=db,
            exclude={"parent_analysis_uuid", "performed_analysis_uuids", "type", "value"},
        )

        # Read the required fields from the database to use with the new observable instance
        new_observable_instance.alert = crud.read(uuid=observable_instance.alert_uuid, db_table=Alert, db=db)
        new_observable_instance.parent_analysis = crud.read(
            uuid=observable_instance.parent_analysis_uuid, db_table=Analysis, db=db
        )

        # Adding an observable instance counts as modifying the alert and the analysis, so they should both get new versions
        new_observable_instance.alert.version = uuid4()
        new_observable_instance.parent_analysis.version = uuid4()

        # Set any performed analyses that were given
        for performed_analysis_uuid in observable_instance.performed_analysis_uuids:
            db_analysis = crud.read(uuid=performed_analysis_uuid, db_table=Analysis, db=db)
            new_observable_instance.performed_analyses.append(db_analysis)

            # This counts as editing the analysis, so it should receive an updated version
            db_analysis.version = uuid4()

        # Set the redirection observable instance if one was given
        if observable_instance.redirection_uuid:
            new_observable_instance.redirection = crud.read(
                uuid=observable_instance.redirection_uuid,
                db_table=ObservableInstance,
                db=db,
            )

        # Lastly, check if the Observable represented by this instance already exists. Create it if it does not.
        db_observable = crud.read_observable(type=observable_instance.type, value=observable_instance.value, db=db)
        if not db_observable:
            db_observable_type = crud.read_by_value(value=observable_instance.type, db_table=ObservableType, db=db)
            db_observable = Observable(type=db_observable_type, value=observable_instance.value)

        # Associate the observable instance with its observable
        new_observable_instance.observable = db_observable

        # Add the new observable instance to the database
        db.add(new_observable_instance)

    # Save the database changes
    crud.commit(db)

    # This will respond with the Content-Location for the last observable instance in the given list.
    response.headers["Content-Location"] = request.url_for("get_observable_instance", uuid=new_observable_instance.uuid)


helpers.api_route_create(router, create_observable_instances)


#
# READ
#


# def get_all_observable_instances(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=ObservableInstance, db=db)


def get_observable_instance(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=ObservableInstance, db=db)


# It does not make sense to have a get_all_observable_instances route at this point (and not without pagination).
# helpers.api_route_read_all(router, get_all_observable_instances, List[ObservableInstanceRead])
helpers.api_route_read(router, get_observable_instance, ObservableInstanceRead)


#
# UPDATE
#


def update_observable_instance(
    uuid: UUID,
    observable_instance: ObservableInstanceUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Update the Node attributes
    db_observable_instance: ObservableInstance = update_node(
        node_update=observable_instance,
        uuid=uuid,
        db_table=ObservableInstance,
        db=db,
    )

    # Get the data that was given in the request and use it to update the database object
    update_data = observable_instance.dict(exclude_unset=True)

    if "context" in update_data:
        db_observable_instance.context = update_data["context"]

    # Any UUIDs given in this list add to the existing ones and do not replace them
    if "performed_analysis_uuids" in update_data:
        for performed_analysis_uuid in update_data["performed_analysis_uuids"]:
            db_analysis = crud.read(uuid=performed_analysis_uuid, db_table=Analysis, db=db)
            db_observable_instance.performed_analyses.append(db_analysis)

            # This counts as editing the analysis, so it should receive an updated version
            db_analysis.version = uuid4()

    if "redirection_uuid" in update_data:
        db_observable_instance.redirection = crud.read(
            uuid=update_data["redirection_uuid"], db_table=ObservableInstance, db=db
        )

        # TODO: Figure out why setting the redirection field above does not set the redirection_uuid
        # the same way it does in the create endpoint.
        db_observable_instance.redirection_uuid = update_data["redirection_uuid"]

    if "time" in update_data:
        db_observable_instance.time = update_data["time"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_observable_instance", uuid=uuid)


helpers.api_route_update(router, update_observable_instance)


#
# DELETE
#


# We currently do not support deleting any Nodes.
