from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.node_directive import (
    NodeDirectiveCreate,
    NodeDirectiveRead,
    NodeDirectiveUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_directive import NodeDirective


router = APIRouter(
    prefix="/node/directive",
    tags=["Node Directive"],
)


#
# CREATE
#


def create_node_directive(
    node_directive: NodeDirectiveCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=node_directive, db_table=NodeDirective, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_directive", uuid=uuid)


helpers.api_route_create(router, create_node_directive)


#
# READ
#


def get_all_node_directives(db: Session = Depends(get_db)):
    return paginate(db, select(NodeDirective))


def get_node_directive(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeDirective, db=db)


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
    crud.update(uuid=uuid, obj=node_directive, db_table=NodeDirective, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_directive", uuid=uuid)


helpers.api_route_update(router, update_node_directive)


#
# DELETE
#


def delete_node_directive(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeDirective, db=db)


helpers.api_route_delete(router, delete_node_directive)
