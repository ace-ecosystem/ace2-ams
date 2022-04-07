import json

from fastapi import APIRouter, Depends, Request, Response
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.observable import ObservableRead, ObservableUpdate
from core.auth import validate_access_token


router = APIRouter(
    prefix="/observable",
    tags=["Observable"],
)


#
# READ
#


def get_observable(uuid: UUID):
    return db_api.get(path=f"/observable/{uuid}")


helpers.api_route_read(router, get_observable, ObservableRead)


#
# UPDATE
#


def update_observable(
    uuid: UUID,
    observable: ObservableUpdate,
    request: Request,
    response: Response,
    claims: dict = Depends(validate_access_token),
):
    db_api.patch(
        path=f"/observable/{uuid}?history_username={claims['sub']}",
        payload=json.loads(observable.json(exclude_unset=True)),
    )

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=uuid)


helpers.api_route_update(router, update_observable)
