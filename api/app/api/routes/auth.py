from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.models.auth import Auth
from api.routes import helpers
from core.auth import (
    create_access_token,
    create_refresh_token,
    refresh_token,
    validate_refresh_token,
)
from core.config import get_settings
from db import crud
from db.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def _set_access_token_cookie(response: Response, access_token: str):
    # The cookie will expire just prior to the actual JWT expiration to avoid a case where the frontend
    # still has the cookie but the JWT inside of it expired.
    access_expiration = get_settings().jwt_access_expire_seconds - 5
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=get_settings().cookies_secure,
        samesite=get_settings().cookies_samesite,
        max_age=access_expiration,
        expires=access_expiration,
    )


def _set_refresh_token_cookie(response: Response, refresh_token: str):
    # The cookie will expire just prior to the actual JWT expiration to avoid a case where the frontend
    # still has the cookie but the JWT inside of it expired.
    #
    # The refresh_token will only be used on the /api/auth API endpoints
    refresh_expiration = get_settings().jwt_refresh_expire_seconds - 5
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=get_settings().cookies_secure,
        samesite=get_settings().cookies_samesite,
        max_age=refresh_expiration,
        expires=refresh_expiration,
        path="/api/auth",
    )


#
# AUTH
#


def auth(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Used to authenticate with the API. Returns an access_token and refresh_token in addition to setting them as
    HttpOnly cookies.
    """

    user = crud.auth(username=form_data.username, password=form_data.password, db=db)

    if user is None or not user.enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(sub=user.username)
    _set_access_token_cookie(response, access_token)

    refresh_token = create_refresh_token(sub=user.username)
    _set_refresh_token_cookie(response, refresh_token)

    # Save the refresh token to the database
    user.refresh_token = refresh_token
    crud.commit(db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


helpers.api_route_auth(
    router=router,
    endpoint=auth,
    response_model=Auth,
    success_desc="Authentication was successful",
    failure_desc="Invalid username or password",
)


#
# AUTH LOGOUT
#


def auth_logout(response: Response):
    """
    The logout endpoint only instructs the browser to delete the access and refresh token cookies. If the API is
    being consumed programatically outside of the browser, then the tokens will remain valid until their expiration.
    """

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/api/auth")


helpers.api_route_auth(
    router=router,
    endpoint=auth_logout,
    method="GET",
    path="/logout",
    success_desc="Logout was successful",
    failure_desc="Invalid access token",
)


#
# AUTH REFRESH
#


def auth_refresh(response: Response, new_tokens: dict = Depends(refresh_token)):
    """
    Used to obtain a new access_token and refresh_token.
    """

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    access_token = new_tokens["access_token"]
    _set_access_token_cookie(response, access_token)

    refresh_token = new_tokens["refresh_token"]
    _set_refresh_token_cookie(response, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


helpers.api_route_auth(
    router=router,
    endpoint=auth_refresh,
    response_model=Auth,
    method="GET",
    path="/refresh",
    success_desc="Token was successfully refreshed",
    failure_desc="Invalid refresh token",
)


#
# AUTH VALIDATE
#


def auth_validate(_: str = Depends(validate_refresh_token)):
    """
    Can be used to periodically ensure your refresh_token is valid. Especially useful for applications relying on
    the HttpOnly cookies that are set during authentication.
    """


helpers.api_route_auth(
    router=router,
    endpoint=auth_validate,
    method="GET",
    path="/validate",
    success_desc="Token is valid",
    failure_desc="Token is invalid",
)
