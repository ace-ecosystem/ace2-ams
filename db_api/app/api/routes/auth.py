from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.routes import helpers
from api_models.auth import Auth
from api_models.user import UserRead
from db import crud
from db.database import get_db
from exceptions.db import ValueNotFoundInDatabase


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

    try:
        return crud.user.auth(username=data.username, password=data.password, db=db)
    except (ValueError, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password") from e


helpers.api_route_auth(
    router=router,
    endpoint=auth,
    response_model=UserRead,
    success_desc="Authentication was successful",
    failure_desc="Invalid username or password",
)
