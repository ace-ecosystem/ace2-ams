from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.node_detection_point import NodeDetectionPointCreate, NodeDetectionPointRead, NodeDetectionPointUpdate
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


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
    db: Session = Depends(get_db),
):
    for node_detection_point in node_detection_points:
        try:
            obj = crud.node_detection_point.create_or_read(model=node_detection_point, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_node_detection_point", uuid=obj.uuid)

    db.commit()

    # Return the UUID of the last detection point
    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_node_detection_points, response_model=Create)


#
# READ
#


def get_node_detection_point(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_detection_point.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Detection point {uuid} does not exist"
        ) from e


helpers.api_route_read(router, get_node_detection_point, NodeDetectionPointRead)


#
# UPDATE
#


def update_node_detection_point(
    uuid: UUID,
    node_detection_point: NodeDetectionPointUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.node_detection_point.update(uuid=uuid, model=node_detection_point, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node detection point {uuid}"
            )
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_detection_point", uuid=uuid)


helpers.api_route_update(router, update_node_detection_point)


#
# DELETE
#


def delete_node_detection_point(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.node_detection_point.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_detection_point)
