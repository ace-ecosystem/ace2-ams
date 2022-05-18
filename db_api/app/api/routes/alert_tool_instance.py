from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.alert_tool_instance import AlertToolInstanceCreate, AlertToolInstanceRead, AlertToolInstanceUpdate
from db import crud
from db.database import get_db
from db.schemas.alert_tool_instance import AlertToolInstance
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/alert/tool/instance",
    tags=["Alert Tool Instance"],
)


#
# CREATE
#


def create_alert_tool_instance(
    create: AlertToolInstanceCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.alert_tool_instance.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_alert_tool_instance", uuid=obj.uuid)


helpers.api_route_create(router, create_alert_tool_instance)


#
# READ
#


def get_all_alert_tool_instances(db: Session = Depends(get_db)):
    return paginate(
        conn=db, query=crud.helpers.build_read_all_query(AlertToolInstance).order_by(AlertToolInstance.value)
    )


def get_alert_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.alert_tool_instance.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=alert_tool_instance, db_table=AlertToolInstance, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update alert tool instance {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_alert_tool_instance", uuid=uuid)


helpers.api_route_update(router, update_alert_tool_instance)


#
# DELETE
#


def delete_alert_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=AlertToolInstance, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete alert tool instance {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_alert_tool_instance)
