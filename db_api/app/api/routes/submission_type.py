from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.submission_type import SubmissionTypeCreate, SubmissionTypeRead, SubmissionTypeUpdate
from db import crud
from db.database import get_db
from db.schemas.submission_type import SubmissionType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/submission/type",
    tags=["Submission Type"],
)


#
# CREATE
#


def create_submission_type(
    create: SubmissionTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.submission_type.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_type", uuid=obj.uuid)


helpers.api_route_create(router, create_submission_type)


#
# READ
#


def get_all_submission_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(SubmissionType).order_by(SubmissionType.value))


def get_submission_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_submission_types, SubmissionTypeRead)
helpers.api_route_read(router, get_submission_type, SubmissionTypeRead)


#
# UPDATE
#


def update_submission_type(
    uuid: UUID,
    submission_type: SubmissionTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=submission_type, db_table=SubmissionType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update submission type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_type", uuid=uuid)


helpers.api_route_update(router, update_submission_type)


#
# DELETE
#


def delete_submission_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=SubmissionType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete submission type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_submission_type)
