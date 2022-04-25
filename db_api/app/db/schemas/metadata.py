from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Metadata(Base):
    __tablename__ = "metadata"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    type = Column(String)

    __mapper_args__ = {"polymorphic_identity": "metadata", "polymorphic_on": type, "with_polymorphic": "*"}

    def serialize(self):
        raise NotImplementedError("A Metadata subclass must implement serialize")
