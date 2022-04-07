from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.node_detection_point import NodeDetectionPointCreate, NodeDetectionPointRead, NodeDetectionPointUpdate
from db import crud
from db.database import get_db
from db.schemas.node import Node
from db.schemas.node_detection_point import NodeDetectionPoint


router = APIRouter(
    prefix="/node/detection_point",
    tags=["Node Detection Point"],
)


#
# CREATE
#


def create_node_detection_points(
    node_detection_points: List[NodeDetectionPointCreate],
    request: Request,
    response: Response,
    history_username: Optional[str] = None,
    db: Session = Depends(get_db),
):
    for node_detection_point in node_detection_points:
        # Create the new node detection point
        new_detection_point = NodeDetectionPoint(**node_detection_point.dict())

        # Make sure the node actually exists
        db_node: Node = crud.read(uuid=node_detection_point.node_uuid, db_table=Node, db=db)

        # This counts a modifying the node, so it should receive a new version.
        crud.update_node_version(node=db_node, db=db)

        # Save the new detection point to the database
        db.add(new_detection_point)
        crud.commit(db)

        # Add an entry to the correct history table based on the node_type.
        # Even though this is creating a detection point, we treat it as though it is
        # modifying the node for history tracking purposes.
        if history_username:
            crud.record_node_update_history(
                record_node=db_node,
                action_by=crud.read_user_by_username(username=history_username, db=db),
                diffs=[
                    crud.Diff(
                        field="detection_points", added_to_list=[node_detection_point.value], removed_from_list=[]
                    )
                ],
                db=db,
            )

        response.headers["Content-Location"] = request.url_for(
            "get_node_detection_point", uuid=new_detection_point.uuid
        )

    # Return the UUID of the last detection point
    return {"uuid": new_detection_point.uuid}


helpers.api_route_create(router, create_node_detection_points, response_model=Create)


#
# READ
#


def get_node_detection_point(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeDetectionPoint, db=db)


helpers.api_route_read(router, get_node_detection_point, NodeDetectionPointRead)


#
# UPDATE
#


def update_node_detection_point(
    uuid: UUID,
    node_detection_point: NodeDetectionPointUpdate,
    request: Request,
    response: Response,
    history_username: Optional[str] = None,
    db: Session = Depends(get_db),
):
    # Read the current node detection point from the database
    db_node_detection_point: NodeDetectionPoint = crud.read(uuid=uuid, db_table=NodeDetectionPoint, db=db)

    # Read the node from the database
    db_node: Node = crud.read(uuid=db_node_detection_point.node_uuid, db_table=Node, db=db)

    # Update the user and timestamp detection point
    db_node_detection_point.insert_time = datetime.utcnow()

    # Set the new detection point value
    diff = crud.Diff(
        field="detection_points",
        added_to_list=[node_detection_point.value],
        removed_from_list=[db_node_detection_point.value],
    )
    db_node_detection_point.value = node_detection_point.value

    crud.commit(db)

    # Modifying the detection point counts as modifying the node, so it should receive a new version
    crud.update_node_version(node=db_node, db=db)

    # Add an entry to the correct history table based on the node_type.
    if history_username:
        crud.record_node_update_history(
            record_node=db_node,
            action_by=crud.read_user_by_username(username=history_username, db=db),
            diffs=[diff],
            db=db,
        )

    response.headers["Content-Location"] = request.url_for("get_node_detection_point", uuid=uuid)


helpers.api_route_update(router, update_node_detection_point)


#
# DELETE
#


def delete_node_detection_point(uuid: UUID, history_username: Optional[str] = None, db: Session = Depends(get_db)):
    # Read the current node detection point from the database to get its value
    db_node: NodeDetectionPoint = crud.read(uuid=uuid, db_table=NodeDetectionPoint, db=db)

    # Update any root node versions
    crud.update_node_version(node=db_node, db=db)

    # Add an entry to the correct history table based on the node_type.
    if history_username:
        crud.record_node_update_history(
            record_node=db_node.node,
            action_by=crud.read_user_by_username(username=history_username, db=db),
            diffs=[crud.Diff(field="detection_points", added_to_list=[], removed_from_list=[db_node.value])],
            db=db,
        )

    # Delete the detection point
    crud.delete(uuid=uuid, db_table=NodeDetectionPoint, db=db)


helpers.api_route_delete(router, delete_node_detection_point)
