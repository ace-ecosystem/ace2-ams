from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import ExcludeConstraint, JSONB, TSTZRANGE, UUID
from sqlalchemy.orm import deferred, relationship

from api_models.analysis import AnalysisNodeTreeRead
from db.schemas.analysis_child_observable_mapping import AnalysisChildObservableMapping
from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_module_type = relationship("AnalysisModuleType", lazy="selectin")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"), nullable=False)

    cached_during = Column(TSTZRANGE(), nullable=False)

    child_observables = relationship("Observable", secondary=AnalysisChildObservableMapping, lazy="selectin")

    # Using deferred means that when you query the Analysis table, you will not select the details field unless
    # you explicitly ask for it. This is so that we can more efficiently load alert trees without selecting
    # all of the analysis details, which can be very large.
    details = deferred(Column(JSONB))

    error_message = Column(String)

    parent_observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), nullable=False)

    run_time = Column(DateTime(timezone=True), index=True, nullable=False)

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {"polymorphic_identity": "analysis", "polymorphic_load": "inline"}

    __table_args__ = (
        Index(
            "analysis_module_type_observable_cached_during_idx",
            analysis_module_type_uuid,
            parent_observable_uuid,
            cached_during,
        ),
        ExcludeConstraint(
            ("analysis_module_type_uuid", "="),
            ("parent_observable_uuid", "="),
            ("cached_during", "&&"),
            name="cached_analysis_uc",
            using="gist",
        ),
    )

    @property
    def cached_until(self):
        return self.cached_during.upper

    def serialize_for_node_tree(self) -> AnalysisNodeTreeRead:
        return AnalysisNodeTreeRead(**self.__dict__)
