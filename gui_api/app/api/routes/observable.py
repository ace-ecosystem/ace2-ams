import json

from fastapi import APIRouter, Request, Response
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.observable import ObservableCreate, ObservableRead, ObservableUpdate


router = APIRouter(
    prefix="/observable",
    tags=["Observable"],
)


#
# CREATE
#


def create_observable(observable: ObservableCreate, request: Request, response: Response):
    result =  db_api.post(path=f"/observable/", payload=json.loads(observable.json()))

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=result["uuid"])



helpers.api_route_create(router, create_observable)


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
):
    db_api.patch(path=f"/observable/{uuid}", payload=json.loads(observable.json(exclude_unset=True)))

    response.headers["Content-Location"] = request.url_for("get_observable", uuid=uuid)


helpers.api_route_update(router, update_observable)
