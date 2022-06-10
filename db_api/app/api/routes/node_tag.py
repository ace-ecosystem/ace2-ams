from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.node_tag import NodeTagCreate, NodeTagRead, NodeTagUpdate
from db import crud
from db.database import get_db
from db.schemas.node_tag import NodeTag
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/node/tag",
    tags=["Node Tag"],
)


#
# CREATE
#


def create_node_tag(
    create: NodeTagCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.node_tag.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_tag", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_node_tag, response_model=Create)


#
# READ
#


def get_all_node_tags(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.node_tag.build_read_all_query())


def get_node_tag(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_tag.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_node_tags, NodeTagRead)
helpers.api_route_read(router, get_node_tag, NodeTagRead)


#
# UPDATE
#


def update_node_tag(
    uuid: UUID,
    node_tag: NodeTagUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=node_tag, db_table=NodeTag, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node tag {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_tag", uuid=uuid)


helpers.api_route_update(router, update_node_tag)


#
# DELETE
#


def delete_node_tag(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=NodeTag, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node tag {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_tag)
