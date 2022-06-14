from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.analysis_metadata import AnalysisMetadataCreate
from api_models.metadata_tag import MetadataTagCreate
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.analysis_metadata import AnalysisMetadata
from db.schemas.observable import Observable


def create_or_read(
    model: AnalysisMetadataCreate,
    db: Session,
    analysis: Optional[Analysis] = None,
    observable: Optional[Observable] = None,
) -> AnalysisMetadata:
    # Read the analysis and observable from the database if needed
    if not analysis:
        analysis = crud.analysis.read_by_uuid(uuid=model.analysis_uuid, db=db)
    if not observable:
        observable = crud.observable.read_by_uuid(uuid=model.observable_uuid, db=db)

    # Create or read the metadata object based on its type
    metadata_object = None
    if model.type == "tag":
        metadata_object = crud.metadata_tag.create_or_read(model=MetadataTagCreate(value=model.value), db=db)

    # Create the analysis metadata object
    if metadata_object:
        obj = AnalysisMetadata(
            analysis_uuid=analysis.uuid, observable_uuid=observable.uuid, metadata_uuid=metadata_object.uuid
        )

        if crud.helpers.create(obj=obj, db=db):
            # Refreshing the analysis object ensures that its analysis_metadata relationship is updated
            db.refresh(analysis)
            return obj

        return read_existing(
            analysis_uuid=analysis.uuid, observable_uuid=observable.uuid, metadata_uuid=metadata_object.uuid, db=db
        )


def read_existing(analysis_uuid: UUID, observable_uuid: UUID, metadata_uuid: UUID, db: Session) -> AnalysisMetadata:
    return (
        db.execute(
            select(AnalysisMetadata).where(
                AnalysisMetadata.analysis_uuid == analysis_uuid,
                AnalysisMetadata.observable_uuid == observable_uuid,
                AnalysisMetadata.metadata_uuid == metadata_uuid,
            )
        )
        .scalars()
        .one()
    )
