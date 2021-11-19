from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import deferred, relationship

from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_uuid = Column(UUID(as_uuid=True), ForeignKey("alert.uuid"), index=True)

    alert = relationship("Alert", foreign_keys=[alert_uuid])

    analysis_module_type = relationship("AnalysisModuleType")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"), nullable=True)

    # Using deferred means that when you query the Analysis table, you will not select the details field unless
    # you explicitly ask for it. This is so that we can more efficiently load alert trees without selecting
    # all of the analysis details, which can be very large.
    details = deferred(Column(JSONB))

    error_message = Column(String)

    # Commenting this out until this functionality is fleshed out
    # event_summary = Column(JSONB)

    # use_alter is used on the ForeignKey so that SQLAlchemy/Alembic uses ALTER to create the foreign key
    # constraint after the tables are created. This is needed because the analysis and observable_instance
    # tables have foreign keys to one another, and there would be no way to determine which table to create first.
    #
    # An "alert" is a combination of analysis and observable instance objects along with some extra metadata.
    # An analysis object is always at the root of an alert, but in the rest of the tree structure, an analysis
    # can be either the parent or a child of an observable instance. Because of this, the parent_uuid
    # foreign key can be nullable, which implies that it is the root analysis object of an alert.
    parent_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_instance.uuid", use_alter=True), nullable=True)

    parent_observable = relationship("ObservableInstance", foreign_keys=[parent_uuid], uselist=False)

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "analysis",
    }
