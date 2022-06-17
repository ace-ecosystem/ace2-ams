from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.metadata_directive import (
    MetadataDirectiveCreate,
    MetadataDirectiveRead,
    MetadataDirectiveUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_directive import MetadataDirective
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/directive",
    tags=["Directive"],
)


#
# CREATE
#


def create_directive(
    create: MetadataDirectiveCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_directive.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_directive", uuid=obj.uuid)


helpers.api_route_create(router, create_directive)


#
# READ
#


def get_all_directives(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_directive.build_read_all_query())


def get_directive(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_directive.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_directives, MetadataDirectiveRead)
helpers.api_route_read(router, get_directive, MetadataDirectiveRead)


#
# UPDATE
#


def update_directive(
    uuid: UUID,
    directive: MetadataDirectiveUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=directive, db_table=MetadataDirective, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update directive {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_directive", uuid=uuid)


helpers.api_route_update(router, update_directive)


#
# DELETE
#


def delete_directive(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataDirective, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete directive {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_directive)
