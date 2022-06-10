import json

from api_models.analysis_module_type import AnalysisModuleTypeUpdate
from db import crud
from tests import factory


def test_update(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(
        cache_seconds=30,
        description="description",
        extended_version={"foo": "bar"},
        manual=False,
        observable_types=["o_type"],
        required_directives=["directive"],
        required_tags=["tag"],
        value="module",
        version="1.0.0",
        db=db,
    )

    assert analysis_module_type.cache_seconds == 30
    assert analysis_module_type.description == "description"
    assert analysis_module_type.extended_version == {"foo": "bar"}
    assert analysis_module_type.manual == False
    assert analysis_module_type.observable_types[0].value == "o_type"
    assert analysis_module_type.required_directives[0].value == "directive"
    assert analysis_module_type.required_tags[0].value == "tag"
    assert analysis_module_type.value == "module"
    assert analysis_module_type.version == "1.0.0"

    result = crud.analysis_module_type.update(
        uuid=analysis_module_type.uuid,
        model=AnalysisModuleTypeUpdate(
            cache_seconds=90,
            description="updated description",
            extended_version=json.dumps({"bar": "baz"}),
            manual=True,
            observable_types=[],
            required_directives=[],
            required_tags=[],
            value="new module",
            version="2.0.0",
        ),
        db=db,
    )

    assert result is True
    assert analysis_module_type.cache_seconds == 90
    assert analysis_module_type.description == "updated description"
    assert analysis_module_type.extended_version == {"bar": "baz"}
    assert analysis_module_type.manual == True
    assert analysis_module_type.observable_types == []
    assert analysis_module_type.required_directives == []
    assert analysis_module_type.required_tags == []
    assert analysis_module_type.value == "new module"
    assert analysis_module_type.version == "2.0.0"


def test_update_conflicting_value_version(db):
    factory.analysis_module_type.create_or_read(
        value="module",
        version="1.0.0",
        db=db,
    )

    obj2 = factory.analysis_module_type.create_or_read(
        value="module2",
        version="1.0.0",
        db=db,
    )

    result = crud.analysis_module_type.update(uuid=obj2.uuid, model=AnalysisModuleTypeUpdate(value="module"), db=db)
    assert result is False
    assert obj2.value == "module2"
