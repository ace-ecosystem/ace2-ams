from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from db.schemas.alert_analysis_mapping import alert_analysis_mapping


def create(analysis_uuid: UUID, submission_uuid: UUID, db: Session):
    with db.begin_nested():
        try:
            db.execute(insert(alert_analysis_mapping).values(alert_uuid=submission_uuid, analysis_uuid=analysis_uuid))
        except IntegrityError:
            db.rollback()
