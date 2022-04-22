import pytest

from sqlalchemy.exc import NoResultFound

from db.crud.observable import create_observable


def test_create_observable_nonexistent_type(db):
    with pytest.raises(NoResultFound):
        create_observable(type="asdf", value="asdf", db=db)
