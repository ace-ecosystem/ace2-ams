from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Metadata(Base):
    __tablename__ = "metadata"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    metadata_type = Column(String)

    __mapper_args__ = {"polymorphic_identity": "metadata", "polymorphic_on": metadata_type, "with_polymorphic": "*"}

    def convert_to_pydantic(self):  # pragma: no cover
        raise NotImplementedError("A Metadata subclass must implement convert_to_pydantic")
