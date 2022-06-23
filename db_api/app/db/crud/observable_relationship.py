from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from api_models.observable_relationship import ObservableRelationshipCreate
from db import crud
from db.schemas.observable import ObservableHistory
from db.schemas.observable_relationship import ObservableRelationship
from db.schemas.observable_relationship_type import ObservableRelationshipType


def create_or_read(model: ObservableRelationshipCreate, db: Session) -> ObservableRelationship:
    # Read the observables from the database
    observable = crud.observable.read_by_uuid(uuid=model.observable_uuid, db=db)
    related_observable = crud.observable.read_by_uuid(uuid=model.related_observable_uuid, db=db)

    obj = ObservableRelationship(
        observable=observable,
        related_observable=related_observable,
        type=crud.observable_relationship_type.read_by_value(value=model.type, db=db),
        uuid=model.uuid,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Adding the relationship counts as modifying the observable, so update its version
        observable.version = uuid4()

        # Add the observable history record
        if model.history_username:
            crud.history.record_update_history(
                history_table=ObservableHistory,
                record=observable,
                action_by=crud.user.read_by_username(username=model.history_username, db=db),
                diffs=[
                    crud.history.Diff(
                        field="relationships", added_to_list=[str(related_observable.uuid)], removed_from_list=[]
                    )
                ],
                db=db,
            )

        db.flush()
        return obj

    return read_by_observable_type(
        observable_uuid=model.observable_uuid,
        related_observable_uuid=model.related_observable_uuid,
        type=model.type,
        db=db,
    )


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read the relationship to get the impacted Node
    relationship = read_by_uuid(uuid=uuid, db=db)

    # Removing the relationship counts as modifying the Node, so update its version
    relationship.observable.version = uuid4()

    # Delete the relationship
    result = crud.helpers.delete(uuid=uuid, db_table=ObservableRelationship, db=db)

    # Add an entry to the appropriate observable history table for deleting the detection point
    crud.history.record_update_history(
        history_table=ObservableHistory,
        record=relationship.observable,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        diffs=[
            crud.history.Diff(
                field="relationships", added_to_list=[], removed_from_list=[str(relationship.related_observable_uuid)]
            )
        ],
        db=db,
    )

    return result


def read_by_uuid(uuid: UUID, db: Session) -> ObservableRelationship:
    return crud.helpers.read_by_uuid(db_table=ObservableRelationship, uuid=uuid, db=db)


def read_by_observable_type(
    observable_uuid: UUID, related_observable_uuid: UUID, type: str, db: Session
) -> ObservableRelationship:
    return (
        db.execute(
            select(ObservableRelationship)
            .join(ObservableRelationshipType)
            .where(
                ObservableRelationship.observable_uuid == observable_uuid,
                ObservableRelationship.related_observable_uuid == related_observable_uuid,
                ObservableRelationshipType.value == type,
            )
        )
        .scalars()
        .one()
    )
