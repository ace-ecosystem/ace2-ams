from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from uuid import UUID

from api.models.node_relationship import NodeRelationshipCreate, NodeRelationshipRead
from api.routes import helpers
from core.auth import validate_access_token
from db import crud
from db.database import get_db
from db.schemas.node import Node
from db.schemas.node_relationship import NodeRelationship
from db.schemas.node_relationship_type import NodeRelationshipType


router = APIRouter(
    prefix="/node/relationship",
    tags=["Node Relationship"],
)


#
# CREATE
#


def create_node_relationship(
    create: NodeRelationshipCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    claims: dict = Depends(validate_access_token),
):
    # Make sure the nodes actually exist
    node: Node = crud.read(uuid=create.node_uuid, db_table=Node, db=db)
    related_node: Node = crud.read(uuid=create.related_node_uuid, db_table=Node, db=db)

    # Make sure the relationship type exists
    type: NodeRelationshipType = crud.read_by_value(value=create.type, db_table=NodeRelationshipType, db=db)

    # Create the relationship
    obj = NodeRelationship(uuid=create.uuid, node_uuid=node.uuid, related_node=related_node, type=type)
    db.add(obj)
    crud.commit(db)

    # Adding the relationship counts as modifying the node, so update its version
    crud.update_node_version(node=node, db=db)

    # Add the node history record
    crud.record_node_update_history(
        record_node=node,
        action_by=crud.read_user_by_username(username=claims["sub"], db=db),
        diffs=[crud.Diff(field="relationships", added_to_list=[str(related_node.uuid)], removed_from_list=[])],
        db=db,
    )

    response.headers["Content-Location"] = request.url_for("get_node_relationship", uuid=obj.uuid)


helpers.api_route_create(router, create_node_relationship)


#
# READ
#


def get_node_relationship(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeRelationship, db=db)


helpers.api_route_read(router, get_node_relationship, NodeRelationshipRead)


#
# DELETE
#


def delete_node_relationship(
    uuid: UUID,
    db: Session = Depends(get_db),
    claims: dict = Depends(validate_access_token),
):
    # Read the relationship to get the impacted node
    relationship: NodeRelationship = crud.read(uuid=uuid, db_table=NodeRelationship, db=db)
    node = relationship.node
    related_node_uuid = relationship.related_node_uuid

    # Removing the relationship counts as modifying the node, so update its version
    crud.update_node_version(node=node, db=db)

    # Delete the relationship
    crud.delete(uuid=uuid, db_table=NodeRelationship, db=db)

    # Add the node history record
    crud.record_node_update_history(
        record_node=node,
        action_by=crud.read_user_by_username(username=claims["sub"], db=db),
        diffs=[crud.Diff(field="relationships", added_to_list=[], removed_from_list=[str(related_node_uuid)])],
        db=db,
    )


helpers.api_route_delete(router, delete_node_relationship)
