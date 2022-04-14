from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.alert_tool import AlertToolCreate, AlertToolRead, AlertToolUpdate
from db import crud
from db.database import get_db
from db.schemas.alert_tool import AlertTool


router = APIRouter(
    prefix="/alert/tool",
    tags=["Alert Tool"],
)


#
# CREATE
#


def create_alert_tool(
    create: AlertToolCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj: AlertTool = crud.create(obj=create, db_table=AlertTool, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_tool", uuid=obj.uuid)


helpers.api_route_create(router, create_alert_tool)


#
# READ
#


def get_all_alert_tools(db: Session = Depends(get_db)):
    return paginate(db, select(AlertTool).order_by(AlertTool.value))


def get_alert_tool(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AlertTool, db=db)


helpers.api_route_read_all(router, get_all_alert_tools, AlertToolRead)
helpers.api_route_read(router, get_alert_tool, AlertToolRead)


#
# UPDATE
#


def update_alert_tool(
    uuid: UUID,
    alert_tool: AlertToolUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=alert_tool, db_table=AlertTool, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_tool", uuid=uuid)


helpers.api_route_update(router, update_alert_tool)


#
# DELETE
#


def delete_alert_tool(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AlertTool, db=db)


helpers.api_route_delete(router, delete_alert_tool)
