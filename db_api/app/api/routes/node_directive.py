from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.node_directive import (
    NodeDirectiveCreate,
    NodeDirectiveRead,
    NodeDirectiveUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.node_directive import NodeDirective
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/node/directive",
    tags=["Node Directive"],
)


#
# CREATE
#


def create_node_directive(
    create: NodeDirectiveCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.node_directive.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_directive", uuid=obj.uuid)


helpers.api_route_create(router, create_node_directive)


#
# READ
#


def get_all_node_directives(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(NodeDirective).order_by(NodeDirective.value))


def get_node_directive(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_directive.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_node_directives, NodeDirectiveRead)
helpers.api_route_read(router, get_node_directive, NodeDirectiveRead)


#
# UPDATE
#


def update_node_directive(
    uuid: UUID,
    node_directive: NodeDirectiveUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=node_directive, db_table=NodeDirective, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node directive {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_directive", uuid=uuid)


helpers.api_route_update(router, update_node_directive)


#
# DELETE
#


def delete_node_directive(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=NodeDirective, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node directive {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_directive)
