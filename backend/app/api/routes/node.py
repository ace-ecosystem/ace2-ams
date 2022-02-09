from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from uuid import UUID, uuid4

from api.models.node import NodeCreate, NodeUpdate, NodeVersion
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node import Node
from db.schemas.node_directive import NodeDirective
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor


router = APIRouter(
    prefix="/node",
    tags=["Node"],
)


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

    if hasattr(node_create, "directives") and node_create.directives:
        db_node.directives = crud.read_by_values(values=node_create.directives, db_table=NodeDirective, db=db)

    if hasattr(node_create, "tags") and node_create.tags:
        db_node.tags = crud.read_by_values(values=node_create.tags, db_table=NodeTag, db=db)

    if hasattr(node_create, "threat_actors") and node_create.threat_actors:
        db_node.threat_actors = crud.read_by_values(values=node_create.threat_actors, db_table=NodeThreatActor, db=db)

    if hasattr(node_create, "threats") and node_create.threats:
        db_node.threats = crud.read_by_values(values=node_create.threats, db_table=NodeThreat, db=db)

    return db_node


def update_node(
    node_update: NodeUpdate, uuid: UUID, db_table: DeclarativeMeta, db: Session
) -> tuple[Node, list[crud.Diff]]:
    """
    Helper function when updating a Node that enforces version matching and updates the attributes inherited from Node.
    """

    # Fetch the Node from the database
    db_node: Node = crud.read(uuid=uuid, db_table=db_table, db=db)

    # Capture all of the diffs that were made (for adding to the history tables)
    diffs: list[crud.Diff] = []

    # Get the data that was given in the request and use it to update the database object
    update_data = node_update.dict(exclude_unset=True)

    # Return an exception if the passed in version does not match the Node's current version
    if "version" in update_data and update_data["version"] != db_node.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Unable to update Node due to version mismatch"
        )

    if "directives" in update_data:
        diffs.append(
            crud.create_diff(
                field="directives", old=[x.value for x in db_node.directives], new=update_data["directives"]
            )
        )

        db_node.directives = crud.read_by_values(values=update_data["directives"], db_table=NodeDirective, db=db)

    if "tags" in update_data:
        diffs.append(crud.create_diff(field="tags", old=[x.value for x in db_node.tags], new=update_data["tags"]))
        db_node.tags = crud.read_by_values(values=update_data["tags"], db_table=NodeTag, db=db)

    if "threat_actors" in update_data:
        diffs.append(
            crud.create_diff(
                field="threat_actors", old=[x.value for x in db_node.threat_actors], new=update_data["threat_actors"]
            )
        )
        db_node.threat_actors = crud.read_by_values(
            values=update_data["threat_actors"], db_table=NodeThreatActor, db=db
        )

    if "threats" in update_data:
        diffs.append(
            crud.create_diff(field="threats", old=[x.value for x in db_node.threats], new=update_data["threats"])
        )
        db_node.threats = crud.read_by_values(values=update_data["threats"], db_table=NodeThreat, db=db)

    # Update the node version
    db_node.version = uuid4()

    return db_node, diffs


#
# READ
#


def get_node_version(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Node, db=db)


helpers.api_route_read(router, get_node_version, NodeVersion, path="/{uuid}/version")
