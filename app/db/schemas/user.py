from sqlalchemy import Boolean, Column, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.user_role_mapping import user_role_mapping


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    default_alert_queue = relationship("AlertQueue")

    default_alert_queue_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_queue.uuid"), nullable=False)

    display_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    enabled = Column(Boolean, default=True, nullable=False)

    password = Column(String, nullable=False)

    roles = relationship("UserRole", secondary=user_role_mapping, passive_deletes=True)

    timezone = Column(String, default="UTC", nullable=False)

    username = Column(String, unique=True, nullable=False)

    refresh_token = Column(String)
