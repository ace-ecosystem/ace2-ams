from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.analysis_module_type import (
    AnalysisModuleTypeCreate,
    AnalysisModuleTypeRead,
    AnalysisModuleTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.node_directive import NodeDirective
from db.schemas.node_tag import NodeTag
from db.schemas.observable_type import ObservableType


router = APIRouter(
    prefix="/analysis/module_type",
    tags=["Analysis Module Type"],
)


#
# CREATE
#


def create_analysis_module_type(
    analysis_module_type: AnalysisModuleTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new analysis module type using the data from the request
    new_analysis_module_type = AnalysisModuleType(**analysis_module_type.dict())

    # If observable types were given, get them from the database and use them in the new analysis module type
    db_observable_types = []
    if analysis_module_type.observable_types:
        db_observable_types = crud.read_by_values(
            values=analysis_module_type.observable_types, db_table=ObservableType, db=db
        )
    new_analysis_module_type.observable_types = db_observable_types

    # If required directives were given, get them from the database and use them in the new analysis module type
    db_required_directives = []
    if analysis_module_type.required_directives:
        db_required_directives = crud.read_by_values(
            values=analysis_module_type.required_directives, db_table=NodeDirective, db=db
        )
    new_analysis_module_type.required_directives = db_required_directives

    # If required tags were given, get them from the database and use them in the new analysis module type
    db_required_tags = []
    if analysis_module_type.required_tags:
        db_required_tags = crud.read_by_values(values=analysis_module_type.required_tags, db_table=NodeTag, db=db)
    new_analysis_module_type.required_tags = db_required_tags

    # Save the new analysis module type to the database
    db.add(new_analysis_module_type)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for(
        "get_analysis_module_type", uuid=new_analysis_module_type.uuid
    )


helpers.api_route_create(router, create_analysis_module_type)


#
# READ
#


def get_all_analysis_module_types(db: Session = Depends(get_db)):
    return paginate(db, select(AnalysisModuleType).order_by(AnalysisModuleType.value, AnalysisModuleType.version))


def get_analysis_module_type(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=AnalysisModuleType, db=db)


helpers.api_route_read_all(router, get_all_analysis_module_types, AnalysisModuleTypeRead)
helpers.api_route_read(router, get_analysis_module_type, AnalysisModuleTypeRead)


#
# UPDATE
#


def update_analysis_module_type(
    uuid: UUID,
    analysis_module_type: AnalysisModuleTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Read the current analysis module type from the database
    db_analysis_module_type: AnalysisModuleType = crud.read(uuid=uuid, db_table=AnalysisModuleType, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = analysis_module_type.dict(exclude_unset=True)

    if "description" in update_data:
        db_analysis_module_type.description = update_data["description"]

    if "extended_version" in update_data:
        db_analysis_module_type.extended_version = update_data["extended_version"]

    if "manual" in update_data:
        db_analysis_module_type.manual = update_data["manual"]

    if "value" in update_data:
        db_analysis_module_type.value = update_data["value"]

    if "observable_types" in update_data:
        db_analysis_module_type.observable_types = crud.read_by_values(
            values=update_data["observable_types"], db_table=ObservableType, db=db
        )

    if "required_directives" in update_data:
        db_analysis_module_type.required_directives = crud.read_by_values(
            values=update_data["required_directives"], db_table=NodeDirective, db=db
        )

    if "required_tags" in update_data:
        db_analysis_module_type.required_tags = crud.read_by_values(
            values=update_data["required_tags"], db_table=NodeTag, db=db
        )

    if "version" in update_data:
        db_analysis_module_type.version = update_data["version"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_analysis_module_type", uuid=uuid)


helpers.api_route_update(router, update_analysis_module_type)


#
# DELETE
#


def delete_analysis_module_type(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=AnalysisModuleType, db=db)


helpers.api_route_delete(router, delete_analysis_module_type)
