from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from uuid import UUID, uuid4

from api.models.node import NodeCreate, NodeUpdate
from db import crud
from db.schemas.node import Node
from db.schemas.node_directive import NodeDirective
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor


def create_node(
    node_create: NodeCreate,
    db_node_type: DeclarativeMeta,
    db: Session,
    exclude: dict = None,
) -> DeclarativeMeta:
    """
    Helper function when creating a new Node that sets the attributes inherited from Node.
    """

    db_node: Node = db_node_type(**node_create.dict(exclude=exclude))

    if node_create.directives:
        db_node.directives = crud.read_by_values(values=node_create.directives, db_table=NodeDirective, db=db)

    if node_create.tags:
        db_node.tags = crud.read_by_values(values=node_create.tags, db_table=NodeTag, db=db)

    if node_create.threat_actor:
        db_node.threat_actor = crud.read_by_value(value=node_create.threat_actor, db_table=NodeThreatActor, db=db)

    if node_create.threats:
        db_node.threats = crud.read_by_values(values=node_create.threats, db_table=NodeThreat, db=db)

    return db_node


def update_node(node_update: NodeUpdate, uuid: UUID, db_table: DeclarativeMeta, db: Session) -> DeclarativeMeta:
    """
    Helper function when updating a Node that enforces version matching and updates the attributes inherited from Node.
    """

    # Fetch the Node from the database
    db_node: Node = crud.read(uuid=uuid, db_table=db_table, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = node_update.dict(exclude_unset=True)

    # Return an exception if the passed in version does not match the Node's current version
    if "version" in update_data and update_data["version"] != db_node.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Unable to update Node due to version mismatch"
        )

    if "directives" in update_data:
        db_node.directives = crud.read_by_values(values=update_data["directives"], db_table=NodeDirective, db=db)

    if "tags" in update_data:
        db_node.tags = crud.read_by_values(values=update_data["tags"], db_table=NodeTag, db=db)

    if "threat_actor" in update_data:
        db_node.threat_actor = crud.read_by_value(value=update_data["threat_actor"], db_table=NodeThreatActor, db=db)

    if "threats" in update_data:
        db_node.threats = crud.read_by_values(values=update_data["threats"], db_table=NodeThreat, db=db)

    # Update the node version
    db_node.version = uuid4()

    return db_node
