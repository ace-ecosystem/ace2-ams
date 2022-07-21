from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from exceptions.db import UuidNotFoundInDatabase


def create(analysis_uuid: UUID, submission_uuid: UUID, db: Session):
    with db.begin_nested():
        try:
            db.execute(
                insert(submission_analysis_mapping).values(submission_uuid=submission_uuid, analysis_uuid=analysis_uuid)
            )
            db.flush()
        except IntegrityError as e:
            db.rollback()

            if "is not present in table" in str(e):
                raise UuidNotFoundInDatabase(
                    f"Could not associate analysis {analysis_uuid} with submission {submission_uuid}: {str(e)}"
                ) from e
