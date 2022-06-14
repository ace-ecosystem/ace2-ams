from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.tag import TagCreate, TagRead, TagUpdate
from db import crud
from db.database import get_db
from db.schemas.tag import Tag
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
)


#
# CREATE
#


def create_tag(
    create: TagCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.tag.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_tag", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_tag, response_model=Create)


#
# READ
#


def get_all_tags(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.tag.build_read_all_query())


def get_tag(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.tag.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_tags, TagRead)
helpers.api_route_read(router, get_tag, TagRead)


#
# UPDATE
#


def update_tag(
    uuid: UUID,
    tag: TagUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=tag, db_table=Tag, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node tag {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_tag", uuid=uuid)


helpers.api_route_update(router, update_tag)


#
# DELETE
#


def delete_tag(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=Tag, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node tag {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_tag)
