from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.helpers import utcnow
from db.schemas.node import Node


class ObservableInstance(Node):
    __tablename__ = "observable_instance"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_uuid = Column(UUID(as_uuid=True), ForeignKey("alert.uuid"), nullable=False, index=True)

    alert = relationship("Alert", foreign_keys=[alert_uuid])

    context = Column(String)

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), nullable=False)

    observable = relationship("Observable", foreign_keys=[observable_uuid])

    # use_alter is used on the ForeignKey so that SQLAlchemy/Alembic uses ALTER to create the foreign key
    # constraint after the tables are created. This is needed because the analysis and observable_instance
    # tables have foreign keys to one another, and there would be no way to determine which table to create first.
    parent_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid", use_alter=True), nullable=False)

    parent_analysis = relationship("Analysis", foreign_keys=[parent_uuid], uselist=False)

    redirection_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_instance.uuid"))

    redirection = relationship("ObservableInstance", foreign_keys=[redirection_uuid], uselist=False)

    time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "observable_instance",
    }
