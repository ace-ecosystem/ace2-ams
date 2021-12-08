from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.alert_tool_instance import AlertToolInstanceCreate, AlertToolInstanceRead, AlertToolInstanceUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.alert_tool_instance import AlertToolInstance


router = APIRouter(
    prefix="/alert/tool/instance",
    tags=["Alert Tool"],
)


#
# CREATE
#


def create_alert_tool_instance(
    alert_tool_instance: AlertToolInstanceCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=alert_tool_instance, db_table=AlertToolInstance, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_tool_instance", uuid=uuid)


helpers.api_route_create(router, create_alert_tool_instance)


#
# READ
#


def get_all_alert_tool_instances(db: Session = Depends(get_db)):
    return paginate(db, select(AlertToolInstance).order_by(AlertToolInstance.value))


def get_alert_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AlertToolInstance, db=db)


helpers.api_route_read_all(router, get_all_alert_tool_instances, AlertToolInstanceRead)
helpers.api_route_read(router, get_alert_tool_instance, AlertToolInstanceRead)


#
# UPDATE
#


def update_alert_tool_instance(
    uuid: UUID,
    alert_tool_instance: AlertToolInstanceUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=alert_tool_instance, db_table=AlertToolInstance, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert_tool_instance", uuid=uuid)


helpers.api_route_update(router, update_alert_tool_instance)


#
# DELETE
#


def delete_alert_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AlertToolInstance, db=db)


helpers.api_route_delete(router, delete_alert_tool_instance)
