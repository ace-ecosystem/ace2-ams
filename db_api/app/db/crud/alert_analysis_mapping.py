from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from uuid import UUID

from db.schemas.alert_analysis_mapping import alert_analysis_mapping


def create(analysis_uuid: UUID, submission_uuid: UUID, db: Session):
    if not mapping_exists(analysis_uuid=analysis_uuid, submission_uuid=submission_uuid, db=db):
        db.execute(insert(alert_analysis_mapping).values(alert_uuid=submission_uuid, analysis_uuid=analysis_uuid))


def mapping_exists(analysis_uuid: UUID, submission_uuid: UUID, db: Session) -> bool:
    return bool(
        db.execute(
            select(alert_analysis_mapping).where(
                alert_analysis_mapping.c.alert_uuid == submission_uuid,
                alert_analysis_mapping.c.analysis_uuid == analysis_uuid,
            )
        )
        .scalars()
        .one_or_none()
    )
