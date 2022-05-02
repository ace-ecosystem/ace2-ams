from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.analysis_module_type import AnalysisModuleTypeCreate
from db import crud
from db.schemas.analysis_module_type import AnalysisModuleType


def create(model: AnalysisModuleTypeCreate, db: Session) -> AnalysisModuleType:
    obj = read_by_value_version(value=model.value, version=model.version, db=db)

    if obj is None:
        obj = AnalysisModuleType(
            cache_seconds=model.cache_seconds,
            description=model.description,
            extended_version=model.extended_version,
            manual=model.manual,
            observable_types=crud.observable_type.read_by_values(values=model.observable_types, db=db),
            required_directives=crud.node_directive.read_by_values(values=model.required_directives, db=db),
            required_tags=crud.node_tag.read_by_values(values=model.required_tags, db=db),
            value=model.value,
            version=model.version,
        )

        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> AnalysisModuleType:
    return crud.helpers.read_by_uuid(db_table=AnalysisModuleType, uuid=uuid, db=db)


def read_by_value_version(value: str, version: str, db: Session) -> AnalysisModuleType:
    return (
        db.execute(
            select(AnalysisModuleType).where(AnalysisModuleType.value == value, AnalysisModuleType.version == version)
        )
        .scalars()
        .one_or_none()
    )
