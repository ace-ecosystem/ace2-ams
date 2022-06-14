from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from api_models.tag import TagRead
from db.schemas.metadata import Metadata


class Tag(Metadata):
    __tablename__ = "tag"

    uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)

    __mapper_args__ = {"polymorphic_identity": "tag", "polymorphic_load": "inline"}

    def convert_to_pydantic(self) -> TagRead:
        return TagRead(**self.__dict__)
