from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.observable_relationship import ObservableRelationshipCreate
from db import crud
from db.schemas.observable_relationship import ObservableRelationship
from db.schemas.observable_relationship_type import ObservableRelationshipType


def create_or_read(model: ObservableRelationshipCreate, db: Session) -> ObservableRelationship:
    # Read the Nodes from the database
    node = crud.node.read_by_uuid(uuid=model.observable_uuid, db=db)
    related_node = crud.node.read_by_uuid(uuid=model.related_observable_uuid, db=db)

    obj = ObservableRelationship(
        node=node,
        related_node=related_node,
        type=crud.observable_relationship_type.read_by_value(value=model.type, db=db),
        uuid=model.uuid,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Adding the relationship counts as modifying the node, so update its version
        crud.node.update_version(node=node, db=db)

        # Add the node history record
        if model.history_username:
            crud.history.record_node_update_history(
                record_node=node,
                action_by=crud.user.read_by_username(username=model.history_username, db=db),
                diffs=[
                    crud.history.Diff(
                        field="relationships", added_to_list=[str(related_node.uuid)], removed_from_list=[]
                    )
                ],
                db=db,
            )

        db.flush()
        return obj

    return read_by_nodes_type(
        node_uuid=model.observable_uuid, related_node_uuid=model.related_observable_uuid, type=model.type, db=db
    )


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read the relationship to get the impacted Node
    relationship = read_by_uuid(uuid=uuid, db=db)

    # Removing the relationship counts as modifying the Node, so update its version
    crud.node.update_version(node=relationship.observable, db=db)

    # Delete the relationship
    result = crud.helpers.delete(uuid=uuid, db_table=ObservableRelationship, db=db)

    # Add an entry to the appropriate node history table for deleting the detection point
    crud.history.record_node_update_history(
        record_node=relationship.observable,
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


def read_by_nodes_type(node_uuid: UUID, related_node_uuid: UUID, type: str, db: Session) -> ObservableRelationship:
    return (
        db.execute(
            select(ObservableRelationship)
            .join(ObservableRelationshipType)
            .where(
                ObservableRelationship.observable_uuid == node_uuid,
                ObservableRelationship.related_observable_uuid == related_node_uuid,
                ObservableRelationshipType.value == type,
            )
        )
        .scalars()
        .one()
    )
