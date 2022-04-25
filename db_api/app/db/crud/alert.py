from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from db.schemas.alert import Alert


def read_alert(uuid: UUID, db: Session) -> Alert:
    return db.execute(select(Alert).where(Alert.uuid == uuid)).scalars().one()
