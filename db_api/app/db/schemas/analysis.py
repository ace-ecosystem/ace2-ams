from sqlalchemy import Column, DateTime, ForeignKey, func, Index, String
from sqlalchemy.dialects.postgresql import ExcludeConstraint, JSONB, TSTZRANGE, UUID
from sqlalchemy.orm import deferred, relationship

from api_models.analysis import AnalysisNodeTreeRead
from db.database import Base
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.observable import Observable


class Analysis(Base):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    analysis_module_type = relationship("AnalysisModuleType", lazy="selectin")

    # An analysis with NULL for analysis_module_type_uuid and parent_observable_uuid signifies it is a Root Analysis
    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"), nullable=True)

    cached_during = Column(TSTZRANGE(), nullable=True)

    child_observables: list[Observable] = relationship(
        "Observable", secondary=analysis_child_observable_mapping, lazy="selectin"
    )

    # Using deferred means that when you query the Analysis table, you will not select the details field unless
    # you explicitly ask for it. This is so that we can more efficiently load alert trees without selecting
    # all of the analysis details, which can be very large.
    details = deferred(Column(JSONB))

    error_message = Column(String)

    # An analysis with NULL for analysis_module_type_uuid and parent_observable_uuid signifies it is a Root Analysis
    parent_observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), nullable=True)

    parent_observable: Observable = relationship("Observable", foreign_keys=[parent_observable_uuid], lazy="selectin")

    run_time = Column(DateTime(timezone=True), index=True, nullable=False)

    stack_trace = Column(String)

    summary = Column(String)

    __table_args__ = (
        Index(
            "analysis_module_type_observable_cached_during_idx",
            analysis_module_type_uuid,
            parent_observable_uuid,
            cached_during,
        ),
        # The PostgreSQL && operator is described here:
        # https://www.postgresql.org/docs/14/functions-array.html
        #
        # It just means that the two ranges overlap.
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

    def convert_to_pydantic(self) -> AnalysisNodeTreeRead:
        return AnalysisNodeTreeRead(**self.__dict__)
