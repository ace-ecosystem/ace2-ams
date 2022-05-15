from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.analysis_module_type import AnalysisModuleTypeCreate
from api_models.node_directive import NodeDirectiveCreate
from api_models.node_tag import NodeTagCreate
from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.analysis_module_type import AnalysisModuleType


def create_or_read(model: AnalysisModuleTypeCreate, db: Session) -> AnalysisModuleType:
    obj = AnalysisModuleType(
        cache_seconds=model.cache_seconds,
        description=model.description,
        extended_version=model.extended_version,
        manual=model.manual,
        observable_types=[
            crud.observable_type.create_or_read(model=ObservableTypeCreate(value=o), db=db)
            for o in model.observable_types
        ],
        required_directives=[
            crud.node_directive.create_or_read(NodeDirectiveCreate(value=d), db=db) for d in model.required_directives
        ],
        required_tags=[crud.node_tag.create_or_read(model=NodeTagCreate(value=t), db=db) for t in model.required_tags],
        value=model.value,
        version=model.version,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value_version(value=model.value, version=model.version, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AnalysisModuleType:
    return crud.helpers.read_by_uuid(db_table=AnalysisModuleType, uuid=uuid, db=db)


def read_by_value_version(value: str, version: str, db: Session) -> AnalysisModuleType:
    return (
        db.execute(
            select(AnalysisModuleType).where(AnalysisModuleType.value == value, AnalysisModuleType.version == version)
        )
        .scalars()
        .one()
    )
