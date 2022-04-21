from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api.routes.node import create_node, update_node
from api_models.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate
from api_models.analysis_details import (
    EmailAnalysisDetails,
    FAQueueAnalysisDetails,
    SandboxAnalysisDetails,
    UserAnalysisDetails,
)
from db import crud
from db.crud.observable import create_observable
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType


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
    # Check for existing/cached analysis
    db_analysis = crud.read_cached_analysis(
        analysis_module_type_uuid=analysis.analysis_module_type_uuid,
        observable_uuid=analysis.parent_observable_uuid,
        db=db,
    )

    if db_analysis is None:
        # Create the new analysis Node using the data from the request
        db_analysis: Analysis = create_node(node_create=analysis, db_node_type=Analysis, db=db, exclude={"node_tree"})

        # Associate the analysis with its analysis module type, parent observable, and child observables
        analysis_module_type: AnalysisModuleType = crud.read(
            uuid=analysis.analysis_module_type_uuid, db_table=AnalysisModuleType, db=db
        )
        db_analysis.analysis_module_type = analysis_module_type

        db_analysis.parent_observable_uuid = analysis.parent_observable_uuid

        db_analysis.child_observables = [
            create_observable(type=o.type, value=o.value, db=db) for o in analysis.child_observables
        ]

        # Calculate the cached_during range based on the AnalysisModuleType's cache_seconds
        db_analysis.cached_during = func.tstzrange(
            analysis.run_time, analysis.run_time + timedelta(seconds=analysis_module_type.cache_seconds), "[)"
        )

        # Validate certain types of analysis details. The GUI depends on specific analysis details
        # when showing event pages. Because of this, we want to ensure that these details conform
        # to what the GUI expects.
        if analysis_module_type.value == "Email Analysis":
            try:
                EmailAnalysisDetails(**analysis.details)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"The Email Analysis details for alert {analysis.node_tree.root_node_uuid} are invalid: {e}",
                )

        elif analysis_module_type.value.startswith("FA Queue"):
            try:
                FAQueueAnalysisDetails(**analysis.details)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"The FA Queue Analysis details for alert {analysis.node_tree.root_node_uuid} are invalid: {e}",
                )

        elif analysis_module_type.value.startswith("Sandbox Analysis"):
            try:
                SandboxAnalysisDetails(**analysis.details)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"The Sandbox Analysis details for alert {analysis.node_tree.root_node_uuid} are invalid: {e}",
                )

        elif analysis_module_type.value == "User Analysis":
            try:
                UserAnalysisDetails(**analysis.details)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"The User Analysis details for alert {analysis.node_tree.root_node_uuid} are invalid: {e}",
                )

        db.add(db_analysis)
        crud.commit(db)

    # Link the analysis to a Node Tree. This happens regardless of whether or not the analysis was cached.
    crud.create_node_tree_leaf(
        node_metadata=analysis.node_tree.node_metadata,
        root_node_uuid=analysis.node_tree.root_node_uuid,
        parent_tree_uuid=analysis.node_tree.parent_tree_uuid,
        node_uuid=db_analysis.uuid,
        db=db,
    )

    crud.commit(db)

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
