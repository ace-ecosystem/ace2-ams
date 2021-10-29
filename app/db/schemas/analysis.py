from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from db.schemas.analysis_observable_instance_mapping import analysis_observable_instance_mapping
from db.schemas.observable_instance_analysis_mapping import observable_instance_analysis_mapping

from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_module_type = relationship("AnalysisModuleType")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"))

    details = Column(JSONB)

    discovered_observables = relationship("ObservableInstance", secondary=analysis_observable_instance_mapping)

    discovered_observable_uuids = association_proxy("discovered_observables", "uuid")

    error_message = Column(String)

    # Commenting this out until this functionality is fleshed out
    # event_summary = Column(JSONB)

    # TODO: Move these comments into the documentation.
    # Analysis can be the parent of an observable instance, and an observable instance can be the parent of an analysis.
    # Because of this circular relationship, both tables cannot have a foreign key to the other, since SQLAlchemy and
    # Alembic would not be able to infer the order in which to create the tables.
    #
    # To resolve this issue, there are two mapping tables:
    #   - analysis_observable_instance_mapping
    #   - observable_instance_analysis_mapping
    #
    # Each mapping table has a column for an analysis_uuid and an observable_instance_uuid, but they serve different
    # purposes. The analysis_observable_instance_mapping table is to keep track of the child observable instances of
    # a given analysis. Since an observable instance can only belong to a single analysis, its column in this mapping
    # table is marked as unique.
    #
    # Similarly, the observable_instance_analysis_mapping table keeps track of the child analyses for a given observable
    # instance. Because an analysis can only belong to a single observable instance, its column in the mapping table is
    # marked as unique.
    #
    # Because of this unique requirements on the mapping tables, the uselist parameter on the relationships is set to
    # False so that it returns a scalar instead of trying to use a list.
    parent_observable = relationship(
        "ObservableInstance",
        secondary=observable_instance_analysis_mapping,
        uselist=False,
    )

    # TODO: Expand this description and move it to the documentation.
    # An association proxy is used so that when you retrieve an Analysis object from the database, you can directly
    # access the UUID of its parent observable (if there is one). This lets the Pydantic models use just the UUID
    # instead of embedding the entire ObservableInstance object.
    parent_observable_uuid = association_proxy("parent_observable", "uuid")

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "analysis",
    }
