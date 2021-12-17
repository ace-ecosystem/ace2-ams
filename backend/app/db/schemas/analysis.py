from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import deferred, relationship

from api.models.analysis import AnalysisNodeTreeRead
from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_module_type = relationship("AnalysisModuleType")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"), nullable=True)

    # Using deferred means that when you query the Analysis table, you will not select the details field unless
    # you explicitly ask for it. This is so that we can more efficiently load alert trees without selecting
    # all of the analysis details, which can be very large.
    details = deferred(Column(JSONB))

    error_message = Column(String)

    # Commenting this out until this functionality is fleshed out
    # event_summary = Column(JSONB)

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {"polymorphic_identity": "analysis", "polymorphic_load": "inline"}

    def serialize_for_node_tree(self) -> AnalysisNodeTreeRead:
        return AnalysisNodeTreeRead(**self.__dict__)
