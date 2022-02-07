from sqlalchemy import Column, DateTime, func, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from db.schemas.helpers import utcnow


"""
NOTE: This is not actually a database table. It does not use table inheritance like the
Node table does. It is used as normal Python class inheritance just so that all of the
various history tables can have the same columns without needing the added overhead of
table inheritance.
"""


class History:
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    action = Column(String, nullable=False)

    action_by = Column(String, nullable=False)

    action_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    record_uuid = Column(UUID(as_uuid=True), index=True, nullable=False)

    field = Column(String)

    diff = Column(JSONB)
