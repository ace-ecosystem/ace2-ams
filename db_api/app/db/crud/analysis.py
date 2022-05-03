from datetime import timedelta
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.analysis import AnalysisCreate
from api_models.analysis_details import (
    EmailAnalysisDetails,
    FAQueueAnalysisDetails,
    SandboxAnalysisDetails,
    UserAnalysisDetails,
)
from db import crud
from db.schemas.analysis import Analysis


def create(model: AnalysisCreate, db: Session) -> Analysis:
    def _validate_analysis_details():
        # The GUI depends on specific analysis details when showing event pages. Because of
        # this, we want to ensure that these details conform to what the GUI expects.
        if analysis_module_type.value == "Email Analysis":
            EmailAnalysisDetails(**model.details)

        elif analysis_module_type.value.startswith("FA Queue"):
            FAQueueAnalysisDetails(**model.details)

        elif analysis_module_type.value.startswith("Sandbox Analysis"):
            SandboxAnalysisDetails(**model.details)

        elif analysis_module_type.value == "User Analysis":
            UserAnalysisDetails(**model.details)

    obj = read_cached(
        analysis_module_type_uuid=model.analysis_module_type_uuid,
        observable_uuid=model.parent_observable_uuid,
        db=db,
    )

    if obj is None:
        analysis_module_type = crud.analysis_module_type.read_by_uuid(uuid=model.analysis_module_type_uuid, db=db)

        _validate_analysis_details()

        obj = Analysis(
            analysis_module_type=analysis_module_type,
            cached_during=func.tstzrange(
                model.run_time, model.run_time + timedelta(seconds=analysis_module_type.cache_seconds), "[)"
            ),
            child_observables=[crud.observable.create(model=co, db=db) for co in model.child_observables],
            details=model.details,
            error_message=model.error_message,
            parent_observable_uuid=model.parent_observable_uuid,
            run_time=model.run_time,
            stack_trace=model.stack_trace,
            summary=model.summary,
        )

        db.add(obj)
        db.flush()

    crud.alert_analysis_mapping.create(analysis_uuid=obj.uuid, root_analysis_uuid=model.root_analysis_uuid, db=db)

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Analysis:
    return crud.helpers.read_by_uuid(db_table=Analysis, uuid=uuid, db=db)


def read_cached(
    analysis_module_type_uuid: UUID,
    observable_uuid: UUID,
    db: Session,
) -> Optional[Analysis]:
    return (
        db.execute(
            select(Analysis).where(
                Analysis.analysis_module_type_uuid == analysis_module_type_uuid,
                Analysis.parent_observable_uuid == observable_uuid,
                Analysis.cached_during.contains(crud.helpers.utcnow()),
            )
        )
        .scalars()
        .one_or_none()
    )
