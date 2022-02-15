from sqlalchemy import Boolean, Column, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.history import HistoryMixin
from db.schemas.user_role_mapping import user_role_mapping


class UserHistory(Base, HistoryMixin):
    __tablename__ = "user_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True, nullable=False)


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    default_alert_queue = relationship("AlertQueue", lazy="selectin")

    default_alert_queue_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_queue.uuid"), nullable=False)

    default_event_queue = relationship("EventQueue", lazy="selectin")

    default_event_queue_uuid = Column(UUID(as_uuid=True), ForeignKey("event_queue.uuid"), nullable=False)

    display_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    enabled = Column(Boolean, default=True, nullable=False)

    # History is lazy loaded and is not included by default when fetching a user from the API.
    history = relationship(
        "UserHistory",
        primaryjoin="UserHistory.record_uuid == User.uuid",
        order_by="UserHistory.action_time",
    )

    password = Column(String, nullable=False)

    roles = relationship("UserRole", secondary=user_role_mapping, passive_deletes=True, lazy="selectin")

    timezone = Column(String, default="UTC", nullable=False)

    training = Column(Boolean, default=True, nullable=False)

    username = Column(String, unique=True, nullable=False)

    refresh_token = Column(String)
