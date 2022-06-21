import json

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from typing import Optional
from uuid import UUID

from api_models.analysis import AnalysisCreate
from api_models.node_detection_point import NodeDetectionPointCreate
from api_models.node_relationship import NodeRelationshipCreate
from api_models.observable import ObservableCreate, ObservableUpdate
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.observable import Observable, ObservableHistory
from db.schemas.observable_type import ObservableType
from exceptions.db import ValueNotFoundInDatabase


def build_read_all_query() -> Select:
    return select(Observable).join(ObservableType).order_by(ObservableType.value, Observable.value)


def create_or_read(
    model: ObservableCreate,
    db: Session,
    parent_analysis: Optional[Analysis] = None,
) -> Observable:
    # Create the new observable Node using the data from the request
    obj: Observable = crud.node.create(
        model=model,
        db_node_type=Observable,
        db=db,
        exclude={
            "analyses",
            "detection_points",
            "history_username",
            "observable_relationships",
            "parent_analysis_uuid",
            "tags",
        },
    )

    # Set the various observable properties
    obj.context = model.context
    obj.expires_on = model.expires_on
    obj.for_detection = model.for_detection
    obj.tags = crud.metadata_tag.read_by_values(values=model.tags, db=db)
    obj.type = crud.observable_type.read_by_value(value=model.type, db=db)
    obj.value = model.value

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

    # Create any detection points that were given
    for detection_point in model.detection_points:
        crud.node_detection_point.create_or_read(
            model=NodeDetectionPointCreate(
                node_uuid=obj.uuid, value=detection_point, history_username=model.history_username
            ),
            db=db,
        )

    # Create any relationships that were given
    for relationship in model.observable_relationships:
        related_observable = read_by_type_value(type=relationship.type, value=relationship.value, db=db)
        crud.node_relationship.create_or_read(
            model=NodeRelationshipCreate(
                history_username=model.history_username,
                node_uuid=obj.uuid,
                related_node_uuid=related_observable.uuid,
                type=relationship.relationship_type,
            ),
            db=db,
        )

    # Create any analyses that were given
    for analysis in model.analyses:
        crud.analysis.create_or_read(
            model=AnalysisCreate(
                details=json.dumps(analysis.details) if analysis.details else None,
                error_message=analysis.error_message,
                stack_trace=analysis.stack_trace,
                summary=analysis.summary,
                analysis_module_type_uuid=analysis.analysis_module_type_uuid,
                child_observables=analysis.child_observables,
                run_time=analysis.run_time,
                submission_uuid=analysis.submission_uuid,
                target_uuid=obj.uuid,
            ),
            db=db,
        )

    # If a parent analysis UUID was given, look up the analysis from the database.
    # Then add the observable to the parent analysis' list of child observables.
    if parent_analysis is None:
        parent_analysis = crud.analysis.read_by_uuid(uuid=model.parent_analysis_uuid, db=db)
    parent_analysis.child_observables.append(obj)

    # If there was any metadata given, it is assumed that it was added by the observable's parent analysis.
    for metadata in model.analysis_metadata:
        crud.analysis_metadata.create_or_read(model=metadata, analysis=parent_analysis, observable=obj, db=db)

    # Update the alert versions that contain the parent analysis
    crud.submission.update_submission_versions(analysis_uuid=parent_analysis.uuid, db=db)

    db.flush()
    return obj


def read_all(db: Session) -> list[Observable]:
    return db.execute(build_read_all_query()).scalars().all()


def read_all_history(uuid: UUID, db: Session) -> list[ObservableHistory]:
    return (
        db.execute(crud.history.build_read_history_query(history_table=ObservableHistory, record_uuid=uuid))
        .scalars()
        .all()
    )


def read_by_type_value(type: str, value: str, db: Session) -> Observable:
    """Returns the Observable with the given type and value if it exists."""

    try:
        return (
            db.execute(
                select(Observable).join(ObservableType).where(ObservableType.value == type, Observable.value == value)
            )
            .scalars()
            .one()
        )
    except NoResultFound as e:
        raise ValueNotFoundInDatabase(
            f'Observable with type "{type}" and value "{value}" was not found in the database.'
        ) from e


def read_by_uuid(uuid: UUID, db: Session) -> Observable:
    return crud.helpers.read_by_uuid(db_table=Observable, uuid=uuid, db=db)


def update(uuid: UUID, model: ObservableUpdate, db: Session) -> bool:
    with db.begin_nested():
        # Update the Node attributes
        observable, diffs = crud.node.update(model=model, uuid=uuid, db_table=Observable, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = model.dict(exclude_unset=True)

        if "context" in update_data:
            diffs.append(crud.history.create_diff(field="context", old=observable.context, new=update_data["context"]))
            observable.context = update_data["context"]

        if "expires_on" in update_data:
            diffs.append(
                crud.history.create_diff(field="expires_on", old=observable.expires_on, new=update_data["expires_on"])
            )
            observable.expires_on = update_data["expires_on"]

        if "for_detection" in update_data:
            diffs.append(
                crud.history.create_diff(
                    field="for_detection", old=observable.for_detection, new=update_data["for_detection"]
                )
            )
            observable.for_detection = update_data["for_detection"]

        if "tags" in update_data:
            diffs.append(
                crud.history.create_diff(
                    field="tags",
                    old=[x.value for x in observable.tags],
                    new=update_data["tags"],
                )
            )
            observable.tags = crud.metadata_tag.read_by_values(values=update_data["tags"], db=db)

        if "type" in update_data:
            diffs.append(crud.history.create_diff(field="type", old=observable.type.value, new=update_data["type"]))
            observable.type = crud.observable_type.read_by_value(value=update_data["type"], db=db)

        if "value" in update_data:
            diffs.append(crud.history.create_diff(field="value", old=observable.value, new=update_data["value"]))
            observable.value = update_data["value"]

        # Try to flush the changes to the database
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            return False

    # Add an observable history entry if the update was successful and the history username was given.
    if model.history_username:
        crud.history.record_node_update_history(
            record_node=observable,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            diffs=diffs,
            db=db,
        )

    return True
