from sqlalchemy import Column, DateTime, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from db.schemas.helpers import utcnow


"""
NOTE: This is not actually a database table. See https://docs.sqlalchemy.org/en/14/orm/declarative_mixins.html
"""


class HistoryMixin:
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    action = Column(String, nullable=False)

    action_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    record_uuid = Column(UUID(as_uuid=True), index=True, nullable=False)

    field = Column(String)

    diff = Column(JSONB)

    snapshot = Column(JSONB, nullable=False)

    @declared_attr
    def action_by_user_uuid(cls):
        return Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True, nullable=False)

    @declared_attr
    def action_by(cls):
        return relationship("User", primaryjoin="User.uuid == %s.action_by_user_uuid" % cls.__name__)


class HasHistory:
    @property
    def history_snapshot(self):  # pragma: no cover
        """Returns the JSON view of the database object that will be saved as the snapshot in the history table"""
        raise NotImplementedError()
