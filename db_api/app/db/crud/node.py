from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from uuid import UUID, uuid4

from api_models.node import NodeCreate, NodeUpdate
from db import crud
from db.schemas.node import Node


def create(
    model: NodeCreate,
    db_node_type: DeclarativeMeta,
    db: Session,
    exclude: dict = None,
) -> DeclarativeMeta:
    obj: Node = db_node_type(**model.dict(exclude=exclude))

    if hasattr(model, "directives") and model.directives:
        obj.directives = crud.node_directive.read_by_values(values=model.directives, db=db)

    if hasattr(model, "tags") and model.tags:
        obj.tags = crud.node_tag.read_by_values(values=model.tags, db=db)

    if hasattr(model, "threat_actors") and model.threat_actors:
        obj.threat_actors = crud.node_threat_actor.read_by_values(values=model.threat_actors, db=db)

    if hasattr(model, "threats") and model.threats:
        obj.threats = crud.node_threat.read_by_values(values=model.threats, db=db)

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Node:
    return crud.helpers.read_by_uuid(db_table=Node, uuid=uuid, db=db)


def update(
    model: NodeUpdate, uuid: UUID, db_table: DeclarativeMeta, db: Session
) -> tuple[Node, list[crud.history.Diff]]:
    node: Node = crud.helpers.read_by_uuid(db_table=db_table, uuid=uuid, db=db)

    # Capture all of the diffs that were made (for adding to the history tables)
    diffs: list[crud.history.Diff] = []

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    # Return an exception if the passed in version does not match the Node's current version
    if "version" in update_data and update_data["version"] != node.version:
        raise ValueError(f"Node version {update_data['version']} does not match the database version {node.version}")

    if "directives" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="directives", old=[x.value for x in node.directives], new=update_data["directives"]
            )
        )

        node.directives = crud.node_directive.read_by_values(values=update_data["directives"], db=db)

    if "tags" in update_data:
        diffs.append(crud.history.create_diff(field="tags", old=[x.value for x in node.tags], new=update_data["tags"]))
        node.tags = crud.node_tag.read_by_values(values=update_data["tags"], db=db)

    if "threat_actors" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="threat_actors", old=[x.value for x in node.threat_actors], new=update_data["threat_actors"]
            )
        )
        node.threat_actors = crud.node_threat_actor.read_by_values(values=update_data["threat_actors"], db=db)

    if "threats" in update_data:
        diffs.append(
            crud.history.create_diff(field="threats", old=[x.value for x in node.threats], new=update_data["threats"])
        )
        node.threats = crud.node_threat.read_by_values(values=update_data["threats"], db=db)

    # Update the node version
    node.version = uuid4()

    return node, diffs
