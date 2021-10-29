from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from api.models.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.observable_instance import ObservableInstance


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# CREATE
#

# TODO: Create/add a discovered observable to an analysis


def create_analysis(
    analysis: AnalysisCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new analysis Node using the data from the request
    new_analysis: Analysis = create_node(
        node_create=analysis, db_node_type=Analysis, db=db, exclude={"parent_observable_uuid"}
    )

    # If an analysis module type was given, get it from the database to use with the new analysis
    if analysis.analysis_module_type:
        new_analysis.analysis_module_type = crud.read(
            uuid=analysis.analysis_module_type, db_table=AnalysisModuleType, db=db
        )

    # Set the parent observable if one was given
    if analysis.parent_observable_uuid:
        new_analysis.parent_observable = crud.read(
            uuid=analysis.parent_observable_uuid, db_table=ObservableInstance, db=db
        )

        # This counts as editing the observable instance, so it should receive an updated version
        new_analysis.parent_observable.version = uuid4()

    # Save the new analysis to the database
    db.add(new_analysis)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=new_analysis.uuid)


helpers.api_route_create(router, create_analysis)


#
# READ
#


# def get_all_analysis(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=Analysis, db=db)


def get_analysis(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Analysis, db=db)


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
    db_analysis: Analysis = update_node(node_update=analysis, uuid=uuid, db_table=Analysis, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = analysis.dict(exclude_unset=True)

    if "analysis_module_type" in update_data:
        db_analysis_module_type = crud.read(
            uuid=update_data["analysis_module_type"], db_table=AnalysisModuleType, db=db
        )
        db_analysis.analysis_module_type = db_analysis_module_type

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
