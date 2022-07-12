from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.analysis_summary_detail import AnalysisSummaryDetailCreate, AnalysisSummaryDetailUpdate
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.analysis_summary_detail import AnalysisSummaryDetail
from exceptions.db import ValueNotFoundInDatabase


def create_or_read(model: AnalysisSummaryDetailCreate, db: Session, analysis: Analysis = None) -> AnalysisSummaryDetail:
    # Make sure the analysis exists if one was not passed in
    if analysis is None:
        analysis = crud.analysis.read_by_uuid(uuid=model.analysis_uuid, db=db)

    obj = AnalysisSummaryDetail(
        analysis_uuid=analysis.uuid,
        content=model.content,
        header=model.header,
        format=crud.format.read_by_value(value=model.format, db=db),
        uuid=model.uuid,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Refresh the analysis object so that its summary_details relationship is updated
        db.refresh(analysis)

        return obj

    return read_by_analysis_header_content(
        analysis_uuid=analysis.uuid, header=model.header, content=model.content, db=db
    )


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=AnalysisSummaryDetail, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AnalysisSummaryDetail:
    return crud.helpers.read_by_uuid(db_table=AnalysisSummaryDetail, uuid=uuid, db=db)


def read_by_analysis_header_content(
    analysis_uuid: UUID, header: str, content: str, db: Session
) -> AnalysisSummaryDetail:
    try:
        return (
            db.execute(
                select(AnalysisSummaryDetail).where(
                    AnalysisSummaryDetail.analysis_uuid == analysis_uuid,
                    AnalysisSummaryDetail.header == header,
                    AnalysisSummaryDetail.content == content,
                )
            )
            .scalars()
            .one()
        )
    except NoResultFound as e:
        raise ValueNotFoundInDatabase(
            f"The '{header}': '{content}' summary detail for analysis {analysis_uuid} was not found in the {AnalysisSummaryDetail.__tablename__} table."
        ) from e


def update(uuid: UUID, model: AnalysisSummaryDetailUpdate, db: Session) -> bool:
    with db.begin_nested():
        # Read the current object
        obj = read_by_uuid(uuid=uuid, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = model.dict(exclude_unset=True)

        if "content" in update_data:
            obj.content = update_data["content"]

        if "format" in update_data:
            obj.format = crud.format.read_by_value(value=update_data["format"], db=db)

        if "header" in update_data:
            obj.header = update_data["header"]

        # Try to flush the changes to the database
        try:
            db.flush()
            return True
        except IntegrityError:
            db.rollback()
            return False
