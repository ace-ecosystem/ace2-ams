import pytest

from db import crud
from exceptions.db import ValueNotFoundInDatabase
from tests import factory


#
# INVALID TESTS
#


def test_read_nonexistent_user(db):
    with pytest.raises(ValueNotFoundInDatabase):
        crud.user.read_by_username(username="user", db=db)


#
# VALID TESTS
#


def test_filter_by_enabled(db):
    user1 = factory.user.create_or_read(username="user1", enabled=False, db=db)
    factory.user.create_or_read(username="user2", enabled=True, db=db)

    result = crud.user.read_all(enabled=False, db=db)
    assert result == [user1]


def test_filter_by_username(db):
    user1 = factory.user.create_or_read(username="user1", db=db)
    factory.user.create_or_read(username="user2", db=db)

    result = crud.user.read_all(username="user1", db=db)
    assert result == [user1]
