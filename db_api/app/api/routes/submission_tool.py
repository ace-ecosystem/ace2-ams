from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.submission_tool import SubmissionToolCreate, SubmissionToolRead, SubmissionToolUpdate
from db import crud
from db.database import get_db
from db.schemas.submission_tool import SubmissionTool
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/submission/tool",
    tags=["Submission Tool"],
)


#
# CREATE
#


def create_submission_tool(
    create: SubmissionToolCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.submission_tool.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_tool", uuid=obj.uuid)


helpers.api_route_create(router, create_submission_tool)


#
# READ
#


def get_all_submission_tools(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(SubmissionTool).order_by(SubmissionTool.value))


def get_submission_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission_tool.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_submission_tools, SubmissionToolRead)
helpers.api_route_read(router, get_submission_tool, SubmissionToolRead)


#
# UPDATE
#


def update_submission_tool(
    uuid: UUID,
    submission_tool: SubmissionToolUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=submission_tool, db_table=SubmissionTool, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update submission tool {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_tool", uuid=uuid)


helpers.api_route_update(router, update_submission_tool)


#
# DELETE
#


def delete_submission_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=SubmissionTool, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete submission tool {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_submission_tool)
