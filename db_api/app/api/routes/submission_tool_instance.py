from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.submission_tool_instance import (
    SubmissionToolInstanceCreate,
    SubmissionToolInstanceRead,
    SubmissionToolInstanceUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.submission_tool_instance import SubmissionToolInstance
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/submission/tool/instance",
    tags=["Submission Tool Instance"],
)


#
# CREATE
#


def create_submission_tool_instance(
    create: SubmissionToolInstanceCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.submission_tool_instance.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_tool_instance", uuid=obj.uuid)


helpers.api_route_create(router, create_submission_tool_instance)


#
# READ
#


def get_all_submission_tool_instances(db: Session = Depends(get_db)):
    return paginate(
        conn=db, query=crud.helpers.build_read_all_query(SubmissionToolInstance).order_by(SubmissionToolInstance.value)
    )


def get_submission_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission_tool_instance.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_submission_tool_instances, SubmissionToolInstanceRead)
helpers.api_route_read(router, get_submission_tool_instance, SubmissionToolInstanceRead)


#
# UPDATE
#


def update_submission_tool_instance(
    uuid: UUID,
    submission_tool_instance: SubmissionToolInstanceUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(
            uuid=uuid, update_model=submission_tool_instance, db_table=SubmissionToolInstance, db=db
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update submission tool instance {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_tool_instance", uuid=uuid)


helpers.api_route_update(router, update_submission_tool_instance)


#
# DELETE
#


def delete_submission_tool_instance(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=SubmissionToolInstance, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete submission tool instance {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_submission_tool_instance)
