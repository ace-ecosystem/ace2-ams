from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


class ObservableRelationshipType(Base):
    __tablename__ = "observable_relationship_type"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)
