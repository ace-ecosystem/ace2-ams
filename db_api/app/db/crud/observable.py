from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.observable import ObservableCreate
from db import crud
from db.schemas.alert import Alert
from db.schemas.alert_analysis_mapping import alert_analysis_mapping
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


def create_or_read(
    model: ObservableCreate,
    db: Session,
) -> Observable:
    obj = Observable(
        context=model.context,
        expires_on=model.expires_on,
        for_detection=model.for_detection,
        redirection=create_or_read(model=model.redirection, db=db) if model.redirection else None,
        time=model.time,
        type=crud.observable_type.read_by_value(value=model.type, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Add an observable history entry if the history username was given. This would typically only be
        # supplied by the GUI when an analyst creates a manual alert or adds an observable to an alert.
        if model.history_username is not None:
            crud.history.record_node_create_history(
                record_node=obj,
                action_by=crud.user.read_by_username(username=model.history_username, db=db),
                db=db,
            )
    else:
        obj = read_by_type_value(type=model.type, value=model.value, db=db)

    for analysis in model.analyses:
        analysis.target_uuid = obj.uuid

        crud.analysis.create_or_read(model=analysis, db=db)

    return obj


def read_by_type_value(type: str, value: str, db: Session) -> Observable:
    """Returns the Observable with the given type and value if it exists."""

    return (
        db.execute(
            select(Observable).join(ObservableType).where(ObservableType.value == type, Observable.value == value)
        )
        .scalars()
        .one()
    )


def read_by_uuid(uuid: UUID, db: Session) -> Observable:
    return crud.helpers.read_by_uuid(db_table=Observable, uuid=uuid, db=db)


def update_version(uuid: UUID, db: Session):
    """Updates the given observable's version as well as any alerts' versions that contain this observable"""

    # Update the observable's version
    observable = read_by_uuid(uuid=uuid, db=db)
    crud.node.update_version(node=observable, db=db)

    # Query the database for every alert that contains this observable
    query = (
        select(Alert)
        .join(
            alert_analysis_mapping,
            onclause=alert_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid,
        )
        .join(
            analysis_child_observable_mapping,
            onclause=analysis_child_observable_mapping.c.observable_uuid == uuid,
        )
    )

    alerts: list[Alert] = db.execute(query).unique().scalars().all()

    # Update each alert's version
    for alert in alerts:
        crud.node.update_version(node=alert, db=db)

    db.flush()
