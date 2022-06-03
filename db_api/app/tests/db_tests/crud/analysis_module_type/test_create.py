import json

from api_models.analysis_module_type import AnalysisModuleTypeCreate
from db import crud


#
# VALID TESTS
#


def test_create(db):
    obj = crud.analysis_module_type.create_or_read(
        model=AnalysisModuleTypeCreate(
            cache_seconds=30,
            description="test description",
            extended_version=json.dumps({"foo": "bar"}),
            manual=True,
            observable_types=["test_type"],
            required_directives=["test_directive"],
            required_tags=["test_tag"],
            value="test_module",
            version="2.0.0",
        ),
        db=db,
    )

    assert obj.cache_seconds == 30
    assert obj.description == "test description"
    assert obj.extended_version == {"foo": "bar"}
    assert obj.manual == True
    assert obj.observable_types[0].value == "test_type"
    assert obj.required_directives[0].value == "test_directive"
    assert obj.required_tags[0].value == "test_tag"
    assert obj.value == "test_module"
    assert obj.version == "2.0.0"


def test_create_duplicate(db):
    obj = crud.analysis_module_type.create_or_read(
        model=AnalysisModuleTypeCreate(value="test_module", version="1.0.0"), db=db
    )

    obj2 = crud.analysis_module_type.create_or_read(
        model=AnalysisModuleTypeCreate(value="test_module", version="1.0.0"), db=db
    )

    assert obj2.uuid == obj.uuid
