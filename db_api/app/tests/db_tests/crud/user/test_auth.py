import pytest

from api_models.auth import Auth, ValidateRefreshToken
from db import crud
from exceptions.db import ReusedToken, UserIsDisabled
from tests import factory


#
# INVALID TESTS
#


def test_auth_wrong_password(db):
    factory.user.create_or_read(username="user", password="password", db=db)
    with pytest.raises(ValueError):
        crud.user.auth(auth=Auth(new_refresh_token="asdf", password="wrong password", username="user"), db=db)


def test_validate_refresh_token_disabled_user(db):
    user = factory.user.create_or_read(username="user", enabled=False, db=db)
    with pytest.raises(UserIsDisabled):
        crud.user.validate_refresh_token(
            data=ValidateRefreshToken(username="user", refresh_token=user.refresh_token, new_refresh_token="asdf"),
            db=db,
        )


def test_validate_refresh_token_reused_token(db):
    factory.user.create_or_read(username="user", db=db)
    with pytest.raises(ReusedToken):
        crud.user.validate_refresh_token(
            data=ValidateRefreshToken(username="user", refresh_token="oldtoken", new_refresh_token="asdf"),
            db=db,
        )


#
# VALID TESTS
#


def test_auth(db):
    user = factory.user.create_or_read(username="user", password="password", db=db)
    assert crud.user.auth(auth=Auth(new_refresh_token="asdf", password="password", username="user"), db=db) == user


def test_validate_refresh_token(db):
    user = factory.user.create_or_read(username="user", db=db)
    assert (
        crud.user.validate_refresh_token(
            data=ValidateRefreshToken(username="user", refresh_token=user.refresh_token, new_refresh_token="asdf"),
            db=db,
        )
        == user
    )
