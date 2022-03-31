from sqlalchemy import DateTime, Column, func
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base
from db.schemas.helpers import utcnow


class Seed(Base):
    __tablename__ = "seed"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    seed_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)
