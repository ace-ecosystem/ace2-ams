from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from api_models.auth import Auth, AuthResponse
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


#
# AUTH
#


def auth(data: Auth, db: Session = Depends(get_db)):
    """
    Used by the GUI API to verify user login information.
    """

    user: Optional[User] = crud.auth(username=data.username, password=data.password, db=db)

    if user is None or not user.enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Save the new refresh token to the database
    user.refresh_token = data.new_refresh_token
    crud.commit(db)


helpers.api_route_auth(
    router=router,
    endpoint=auth,
    response_model=AuthResponse,
    success_desc="Authentication was successful",
    failure_desc="Invalid username or password",
)
