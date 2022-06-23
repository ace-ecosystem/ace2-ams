from sqlalchemy import func, Column, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class SubmissionComment(Base):
    __tablename__ = "submission_comment"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    insert_time = Column(DateTime, server_default=utcnow())

    submission_uuid = Column(UUID(as_uuid=True), ForeignKey("submission.uuid"), index=True)

    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    user = relationship("User", foreign_keys=[user_uuid])

    value = Column(String, nullable=False)

    __table_args__ = (
        Index(
            "submission_comment_value_trgm",
            value,
            postgresql_ops={"value": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
        UniqueConstraint("submission_uuid", "value", name="submission_value_uc"),
    )
