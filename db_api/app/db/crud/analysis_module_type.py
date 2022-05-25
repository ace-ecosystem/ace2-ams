from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.analysis_module_type import AnalysisModuleTypeCreate, AnalysisModuleTypeUpdate
from api_models.node_directive import NodeDirectiveCreate
from api_models.node_tag import NodeTagCreate
from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.analysis_module_type import AnalysisModuleType


def build_read_all_query() -> Select:
    return select(AnalysisModuleType).order_by(AnalysisModuleType.value, AnalysisModuleType.version)


def create_or_read(model: AnalysisModuleTypeCreate, db: Session) -> AnalysisModuleType:
    obj = AnalysisModuleType(
        cache_seconds=model.cache_seconds,
        description=model.description,
        extended_version=model.extended_version,
        manual=model.manual,
        observable_types=[
            crud.observable_type.create_or_read(model=ObservableTypeCreate(value=o), db=db)
            for o in set(model.observable_types)
        ],
        required_directives=[
            crud.node_directive.create_or_read(NodeDirectiveCreate(value=d), db=db)
            for d in set(model.required_directives)
        ],
        required_tags=[
            crud.node_tag.create_or_read(model=NodeTagCreate(value=t), db=db) for t in set(model.required_tags)
        ],
        uuid=model.uuid,
        value=model.value,
        version=model.version,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value_version(value=model.value, version=model.version, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AnalysisModuleType:
    return crud.helpers.read_by_uuid(db_table=AnalysisModuleType, uuid=uuid, db=db)


def read_by_value_latest_version(value: str, db: Session) -> AnalysisModuleType:
    return (
        db.execute(
            select(AnalysisModuleType)
            .where(AnalysisModuleType.value == value)
            .order_by(AnalysisModuleType.version.desc())
        )
        .scalars()
        .first()
    )


def read_by_value_version(value: str, version: str, db: Session) -> AnalysisModuleType:
    return (
        db.execute(
            select(AnalysisModuleType).where(AnalysisModuleType.value == value, AnalysisModuleType.version == version)
        )
        .scalars()
        .one()
    )


def update(uuid: UUID, model: AnalysisModuleTypeUpdate, db: Session) -> bool:
    obj = read_by_uuid(uuid=uuid, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    with db.begin_nested():
        try:
            if "cache_seconds" in update_data:
                obj.cache_seconds = update_data["cache_seconds"]

            if "description" in update_data:
                obj.description = update_data["description"]

            if "extended_version" in update_data:
                obj.extended_version = update_data["extended_version"]

            if "manual" in update_data:
                obj.manual = update_data["manual"]

            if "observable_types" in update_data:
                obj.observable_types = crud.observable_type.read_by_values(
                    values=update_data["observable_types"], db=db
                )

            if "required_directives" in update_data:
                obj.required_directives = crud.node_directive.read_by_values(
                    values=update_data["required_directives"], db=db
                )

            if "required_tags" in update_data:
                obj.required_tags = crud.node_tag.read_by_values(values=update_data["required_tags"], db=db)

            if "value" in update_data:
                obj.value = update_data["value"]

            if "version" in update_data:
                obj.version = update_data["version"]

            db.flush()
            return True
        except IntegrityError:
            db.rollback()

    return False
