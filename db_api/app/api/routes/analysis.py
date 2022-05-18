from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate
from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# CREATE
#


def create_analysis(
    analysis: AnalysisCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_analysis = crud.analysis.create_or_read(model=analysis, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=db_analysis.uuid)


helpers.api_route_create(router, create_analysis)


#
# READ
#


# def get_all_analysis(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=Analysis, db=db)


def get_analysis(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Analysis, undefer_column="details", db=db)


# It does not make sense to have a get_all_analysis route at this point (and certainly not without pagination).
# helpers.api_route_read_all(router, get_all_analysis, List[AnalysisRead])
helpers.api_route_read(router, get_analysis, AnalysisRead)


#
# UPDATE
#


def update_analysis(
    uuid: UUID,
    analysis: AnalysisUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Update the Node attributes
    db_analysis, diffs = update_node(node_update=analysis, uuid=uuid, db_table=Analysis, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = analysis.dict(exclude_unset=True)

    if "details" in update_data:
        db_analysis.details = update_data["details"]

    if "error_message" in update_data:
        db_analysis.error_message = update_data["error_message"]

    if "stack_trace" in update_data:
        db_analysis.stack_trace = update_data["stack_trace"]

    if "summary" in update_data:
        db_analysis.summary = update_data["summary"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=uuid)


helpers.api_route_update(router, update_analysis)


#
# DELETE
#


# We currently do not support deleting any Nodes.
