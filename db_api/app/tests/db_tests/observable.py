import pytest

from sqlalchemy.exc import NoResultFound

from db import crud


def test_create_observable_nonexistent_type(db):
    with pytest.raises(NoResultFound):
        crud.observable.create_or_read(type="asdf", value="asdf", db=db)
