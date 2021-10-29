from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from db.schemas.analysis_observable_instance_mapping import analysis_observable_instance_mapping
from db.schemas.observable_instance_analysis_mapping import observable_instance_analysis_mapping
from db.schemas.helpers import utcnow
from db.schemas.node import Node


class ObservableInstance(Node):
    __tablename__ = "observable_instance"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_uuid = Column(UUID(as_uuid=True), ForeignKey("alert.uuid"))

    alert = relationship("Alert", foreign_keys=[alert_uuid])

    context = Column(String)

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), nullable=False)

    observable = relationship("Observable", foreign_keys=[observable_uuid])

    parent_analysis = relationship("Analysis", secondary=analysis_observable_instance_mapping, uselist=False)

    parent_analysis_uuid = association_proxy("parent_analysis", "uuid")

    performed_analyses = relationship("Analysis", secondary=observable_instance_analysis_mapping)

    performed_analysis_uuids = association_proxy("performed_analyses", "uuid")

    redirection_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_instance.uuid"))

    redirection = relationship("ObservableInstance", foreign_keys=[redirection_uuid], uselist=False)

    time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "observable_instance",
    }
