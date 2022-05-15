from sqlalchemy.orm import Session

from api_models.analysis_module_type import AnalysisModuleTypeCreate
from db import crud


def create_or_read(
    value: str,
    version: str,
    db: Session,
    cache_seconds: int = 300,
    manual: bool = False,
    observable_types: list[str] = None,
    required_directives: list[str] = None,
    required_tags: list[str] = None,
):
    if observable_types is None:
        observable_types = []

    if required_directives is None:
        required_directives = []

    if required_tags is None:
        required_tags = []

    return crud.analysis_module_type.create_or_read(
        model=AnalysisModuleTypeCreate(
            cache_seconds=cache_seconds,
            manual=manual,
            observable_types=observable_types,
            required_directives=required_directives,
            required_tags=required_tags,
            value=value,
            version=version,
        ),
        db=db,
    )
