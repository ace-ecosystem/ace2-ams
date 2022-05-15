from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_remediation import (
    EventRemediationCreate,
    EventRemediationRead,
    EventRemediationUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_remediation import EventRemediation
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/event/remediation",
    tags=["Event Remediation"],
)


#
# CREATE
#


def create_event_remediation(
    create: EventRemediationCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.event_remediation.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_remediation", uuid=obj.uuid)


helpers.api_route_create(router, create_event_remediation)


#
# READ
#


def get_all_event_remediations(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventRemediation).order_by(EventRemediation.value))


def get_event_remediation(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_remediation.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_remediations, EventRemediationRead)
helpers.api_route_read(router, get_event_remediation, EventRemediationRead)


#
# UPDATE
#


def update_event_remediation(
    uuid: UUID,
    event_remediation: EventRemediationUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_remediation, db_table=EventRemediation, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event remediation {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_event_remediation", uuid=uuid)


helpers.api_route_update(router, update_event_remediation)


#
# DELETE
#


def delete_event_remediation(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventRemediation, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event remediation {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_event_remediation)
