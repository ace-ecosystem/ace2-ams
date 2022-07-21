from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.analysis_status import AnalysisStatusCreate, AnalysisStatusUpdate
from db import crud
from db.schemas.analysis_status import AnalysisStatus


def build_read_all_query() -> Select:
    return select(AnalysisStatus).order_by(AnalysisStatus.value)


def create_or_read(model: AnalysisStatusCreate, db: Session) -> AnalysisStatus:
    obj = AnalysisStatus(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=AnalysisStatus, db=db)


def read_all(db: Session) -> list[AnalysisStatus]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> AnalysisStatus:
    return crud.helpers.read_by_uuid(db_table=AnalysisStatus, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> AnalysisStatus:
    return crud.helpers.read_by_value(db_table=AnalysisStatus, value=value, db=db)


def update(uuid: UUID, model: AnalysisStatusUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=AnalysisStatus, db=db)
