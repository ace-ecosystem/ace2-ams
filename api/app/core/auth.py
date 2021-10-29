import uuid

from collections.abc import Mapping
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, jwt, JWTError
from passlib.hash import bcrypt_sha256
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Dict, Mapping, Optional

from core.config import get_settings
from db.database import get_db
from db.schemas.user import User


# This class is copy/pasted from fastapi.security.OAuth2PasswordBearer with slight modifications
# so that it pulls the token from the request cookies OR the Authorization header.
class OAuth2PasswordBearerCookieOrHeader(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        token_type: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.token_type = token_type
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # The Authorization header will takes precedence over cookies
        authorization: str = request.headers.get("Authorization") or request.cookies.get(self.token_type)  # type: ignore
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            # if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # else:
        #     return None
        return param


oauth2_access_scheme = OAuth2PasswordBearerCookieOrHeader(tokenUrl="/api/auth", token_type="access_token")
oauth2_refresh_scheme = OAuth2PasswordBearerCookieOrHeader(tokenUrl="/api/auth", token_type="refresh_token")


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    """
    Generic function to generate and return a JWT.

    Args:
        token_type: "access_token" or "refresh_token"
        lifetime: a datetime timedelta representing how long the token should remain valid
        sub: the subject to use for the token claims (username by default)
    """

    payload = {
        "type": token_type,
        "exp": datetime.utcnow() + lifetime,
        "iat": datetime.utcnow(),
        "sub": sub,
        # A UUID is used so that if the token is generated at the exact same time it will be different
        "ace2_uuid": str(uuid.uuid4()),
    }

    return jwt.encode(payload, get_settings().jwt_secret, algorithm=get_settings().jwt_algorithm)


def create_access_token(sub: str) -> str:
    """
    Generates and returns an access_token JWT that is used to authenticate to the API endpoints.

    Args:
        sub: the subject to use for the token claims (username by default)
    """

    return _create_token(
        token_type="access_token",
        lifetime=timedelta(seconds=get_settings().jwt_access_expire_seconds),
        sub=sub,
    )


def create_refresh_token(sub: str) -> str:
    """
    Generates and returns a refresh_token JWT that is used to obtain a new access_token.

    Args:
        sub: the subject to use for the token claims (username by default)
    """

    return _create_token(
        token_type="refresh_token",
        lifetime=timedelta(seconds=get_settings().jwt_refresh_expire_seconds),
        sub=sub,
    )


def decode_token(token: str) -> Mapping:
    """
    Decodes the JWT and returns its claims.

    Args:
        token: an access_token or refresh_token
    """

    return jwt.decode(token, get_settings().jwt_secret, algorithms=[get_settings().jwt_algorithm])


def hash_password(password: str) -> str:
    """
    Salts and hashes the given password.

    Args:
        password: the plaintext password to hash
    """

    return bcrypt_sha256.hash(password)


def refresh_token(db: Session = Depends(get_db), refresh_token: str = Depends(oauth2_refresh_scheme)) -> dict:
    """
    Generates and returns a new access_token if the given refresh_token is valid and not expired.

    This is designed to be used with FastAPI dependency injection so that the token is validated before the refresh auth
    API endpoint is invoked.

    Args:
        db: a Session to the database
        refresh_token: a valid refresh_token

    Returns:
        a dictionary containing the new access_token and refresh_token
    """

    def _is_refresh_token(claims: Mapping) -> bool:
        return claims["type"] == "refresh_token"

    try:
        claims = decode_token(refresh_token)

        if _is_refresh_token(claims):
            # Make sure the user in the refresh token claims is valid and enabled
            user: User = (
                db.execute(select(User).where(User.username == claims["sub"], User.enabled == True))
                .scalars()
                .one_or_none()
            )
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Check the refresh token against the database to ensure it is valid. If the token does not match, it may mean
            # that someone is trying to use an old refresh token. In this case, remove the current refresh token from the
            # database to require the user to fully log in again.
            if refresh_token != user.refresh_token:
                user.refresh_token = None
                db.commit()

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Reused token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Rotate the refresh token and save it to the database
            new_refresh_token = create_refresh_token(claims["sub"])
            user.refresh_token = new_refresh_token
            db.commit()

            return {"access_token": create_access_token(claims["sub"]), "refresh_token": new_refresh_token}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_access_token(access_token: str = Depends(oauth2_access_scheme)) -> str:
    """
    Validates that the given access_token can be decoded using our secret key, that it is not expired, and
    that it is in fact an access_token and not another type of token.

    This is designed to be used with FastAPI dependency injection so that the token is validated before the API
    endpoints are invoked.

    Args:
        access_token: a valid access_token

    Returns:
        a string representing the "sub" claim from the token (the username by default)
    """

    def _is_access_token(claims: Mapping) -> bool:
        return claims["type"] == "access_token"

    try:
        claims = decode_token(access_token)

        if _is_access_token(claims):
            return claims["sub"]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_refresh_token(refresh_token: str = Depends(oauth2_refresh_scheme)) -> str:
    """
    Validates that the given refresh_token can be decoded using our secret key, that it is not expired, and
    that it is in fact an refresh_token and not another type of token.

    This is designed to be used with FastAPI dependency injection so that the token is validated before the API
    endpoints are invoked.

    Args:
        refresh_token: a valid refresh_token

    Returns:
        a string representing the "sub" claim from the token (the username by default)
    """

    def _is_refresh_token(claims: Mapping) -> bool:
        return claims["type"] == "refresh_token"

    try:
        claims = decode_token(refresh_token)

        if _is_refresh_token(claims):
            return claims["sub"]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies that the given password matches the given hashed password.

    Args:
        password: the plaintext password
        hashed_password: the hashed password used to verify the plaintext password
    """

    return bcrypt_sha256.verify(password, hashed_password)
