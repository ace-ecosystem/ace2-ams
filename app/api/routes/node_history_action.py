from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.node_history_action import (
    NodeHistoryActionCreate,
    NodeHistoryActionRead,
    NodeHistoryActionUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_history_action import NodeHistoryAction


router = APIRouter(
    prefix="/node/history/action",
    tags=["Node History Action"],
)


#
# CREATE
#


def create_node_history_action(
    node_history_action: NodeHistoryActionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=node_history_action, db_table=NodeHistoryAction, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_history_action", uuid=uuid)


helpers.api_route_create(router, create_node_history_action)


#
# READ
#


def get_all_node_history_actions(db: Session = Depends(get_db)):
    return crud.read_all(db_table=NodeHistoryAction, db=db)


def get_node_history_action(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeHistoryAction, db=db)


helpers.api_route_read_all(router, get_all_node_history_actions, List[NodeHistoryActionRead])
helpers.api_route_read(router, get_node_history_action, NodeHistoryActionRead)


#
# UPDATE
#


def update_node_history_action(
    uuid: UUID,
    node_history_action: NodeHistoryActionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=node_history_action, db_table=NodeHistoryAction, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_history_action", uuid=uuid)


helpers.api_route_update(router, update_node_history_action)


#
# DELETE
#


def delete_node_history_action(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeHistoryAction, db=db)


helpers.api_route_delete(router, delete_node_history_action)
