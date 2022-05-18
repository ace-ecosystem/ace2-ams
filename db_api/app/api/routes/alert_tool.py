from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.alert_tool import AlertToolCreate, AlertToolRead, AlertToolUpdate
from db import crud
from db.database import get_db
from db.schemas.alert_tool import AlertTool
from exceptions.db import UuidNotFoundInDatabase


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
    obj = crud.alert_tool.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_alert_tool", uuid=obj.uuid)


helpers.api_route_create(router, create_alert_tool)


#
# READ
#


def get_all_alert_tools(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(AlertTool).order_by(AlertTool.value))


def get_alert_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.alert_tool.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=alert_tool, db_table=AlertTool, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update alert tool {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_alert_tool", uuid=uuid)


helpers.api_route_update(router, update_alert_tool)


#
# DELETE
#


def delete_alert_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=AlertTool, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete alert tool {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_alert_tool)
