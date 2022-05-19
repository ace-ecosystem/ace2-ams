from datetime import timedelta
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.analysis import AnalysisCreate, AnalysisUpdate
from api_models.analysis_details import (
    EmailAnalysisDetails,
    FAQueueAnalysisDetails,
    SandboxAnalysisDetails,
    UserAnalysisDetails,
)
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType


def create_or_read(model: AnalysisCreate, db: Session) -> Analysis:
    # Validate the analysis details
    analysis_module_type = crud.analysis_module_type.read_by_uuid(uuid=model.analysis_module_type_uuid, db=db)
    validate_analysis_details(analysis_module_type=analysis_module_type, details=model.details)

    obj = Analysis(
        analysis_module_type=analysis_module_type,
        # The [) range operator is described here:
        # https://www.postgresql.org/docs/current/rangetypes.html#RANGETYPES-INCLUSIVITY
        #
        # [ mean that the lower bound of the range is inclusive, and ) means that the upper bound of
        # the range is exclusive.
        cached_during=func.tstzrange(
            model.run_time, model.run_time + timedelta(seconds=analysis_module_type.cache_seconds), "[)"
        ),
        details=model.details,
        error_message=model.error_message,
        run_time=model.run_time,
        stack_trace=model.stack_trace,
        summary=model.summary,
        target_uuid=model.target_uuid,
        uuid=model.uuid,
    )

    # If the analysis cannot be created, that implies there is already a cached version
    if not crud.helpers.create(obj=obj, db=db):
        obj = read_cached(
            analysis_module_type_uuid=model.analysis_module_type_uuid,
            observable_uuid=model.target_uuid,
            db=db,
        )

    # Associate the child observables with the analysis
    obj.child_observables = [crud.observable.create_or_read(model=co, db=db) for co in model.child_observables]

    # Associate the analysis with its submission
    crud.alert_analysis_mapping.create(analysis_uuid=obj.uuid, submission_uuid=model.submission_uuid, db=db)

    return obj


def create_root(db: Session) -> Analysis:
    obj = Analysis()

    db.add(obj)
    db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Analysis:
    return crud.helpers.read_by_uuid(db_table=Analysis, uuid=uuid, db=db, undefer_column="details")


def read_cached(
    analysis_module_type_uuid: UUID,
    observable_uuid: UUID,
    db: Session,
) -> Analysis:
    return (
        db.execute(
            select(Analysis).where(
                Analysis.analysis_module_type_uuid == analysis_module_type_uuid,
                Analysis.target_uuid == observable_uuid,
                Analysis.cached_during.contains(crud.helpers.utcnow()),
            )
        )
        .scalars()
        .one()
    )


def update(uuid: UUID, model: AnalysisUpdate, db: Session):
    obj = read_by_uuid(uuid=uuid, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)
    for key in update_data:
        setattr(obj, key, update_data[key])

    db.flush()


def validate_analysis_details(analysis_module_type: AnalysisModuleType, details: Optional[dict]):
    """
    The GUI depends on specific analysis details when showing event pages. Because of this,
    this function is used to ensure these details conform to what the GUI expects.
    """

    if details:
        if analysis_module_type.value == "Email Analysis":
            EmailAnalysisDetails(**details)

        elif analysis_module_type.value.startswith("FA Queue"):
            FAQueueAnalysisDetails(**details)

        elif analysis_module_type.value.startswith("Sandbox Analysis"):
            SandboxAnalysisDetails(**details)

        elif analysis_module_type.value == "User Analysis":
            UserAnalysisDetails(**details)
