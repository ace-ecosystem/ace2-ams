from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.alert_disposition import (
    AlertDispositionCreate,
    AlertDispositionRead,
    AlertDispositionUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.alert_disposition import AlertDisposition
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/alert/disposition",
    tags=["Alert Disposition"],
)


#
# CREATE
#


def create_disposition(
    create: AlertDispositionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.alert_disposition.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=obj.uuid)


helpers.api_route_create(router, create_disposition)


#
# READ
#


def get_all_dispositions(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(AlertDisposition).order_by(AlertDisposition.rank))


def get_disposition(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.alert_disposition.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_dispositions, AlertDispositionRead)
helpers.api_route_read(router, get_disposition, AlertDispositionRead)


#
# UPDATE
#


def update_disposition(
    uuid: UUID,
    disposition: AlertDispositionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.alert_disposition.update(uuid=uuid, model=disposition, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update alert disposition {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_disposition", uuid=uuid)


helpers.api_route_update(router, update_disposition)


#
# DELETE
#


def delete_disposition(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.alert_disposition.delete(uuid=uuid, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete alert disposition {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_disposition)
