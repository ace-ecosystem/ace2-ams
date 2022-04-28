from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from uuid import UUID


def read_by_uuid(db_table: DeclarativeMeta, uuid: UUID, db: Session):
    return db.execute(select(db_table).where(db_table.uuid == uuid)).scalars().one()


def read_by_value(db_table: DeclarativeMeta, value: str, db: Session):
    return db.execute(select(db_table).where(db_table.value == value)).scalars().one_or_none()


def read_by_values(db_table: DeclarativeMeta, values: list[str], db: Session) -> list:
    if not values:
        return []

    unique_values = set(values)
    result = db.execute(select(db_table).where(db_table.value.in_(values))).scalars().all()
    assert len(unique_values) == len(result)
    return result


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
