from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.event_remediation import (
    EventRemediationCreate,
    EventRemediationRead,
    EventRemediationUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.queue import Queue
from db.schemas.event_remediation import EventRemediation


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
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: EventRemediation = crud.create(obj=create, db_table=EventRemediation, db=db, exclude=["queues"])
    obj.queues = queues

    response.headers["Content-Location"] = request.url_for("get_event_remediation", uuid=obj.uuid)


helpers.api_route_create(router, create_event_remediation)


#
# READ
#


def get_all_event_remediations(db: Session = Depends(get_db)):
    return paginate(db, select(EventRemediation).order_by(EventRemediation.value))


def get_event_remediation(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventRemediation, db=db)


helpers.api_route_read_all(router, get_all_event_remediations, EventRemediationRead)
helpers.api_route_read(router, get_event_remediation, EventRemediationRead)


#
# UPDATE
#


def update_event_remediation(
    uuid: UUID,
    update: EventRemediationUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: EventRemediation = crud.read(uuid=uuid, db_table=EventRemediation, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event_remediation", uuid=uuid)


helpers.api_route_update(router, update_event_remediation)


#
# DELETE
#


def delete_event_remediation(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventRemediation, db=db)


helpers.api_route_delete(router, delete_event_remediation)
