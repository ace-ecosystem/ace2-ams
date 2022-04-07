import json

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api import db_api
from api.routes import helpers
from api_models.test import AddTestAlert, AddTestEvent


router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


#
# ADD TEST ALERTS
#


def add_test_alerts(alert: AddTestAlert):
    db_api.post(
        path="/test/add_alerts",
        payload=json.loads(alert.json()),
        expected_status=status.HTTP_204_NO_CONTENT,
        return_json=False,
    )


helpers.api_route_create(
    router,
    add_test_alerts,
    path="/add_alerts",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test alerts were added to the database",
        },
        status.HTTP_403_FORBIDDEN: {"description": "Unable to add test alerts when not running in TESTING mode"},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)


#
# ADD TEST EVENTS
#


def add_test_events(event: AddTestEvent):
    db_api.post(
        path="/test/add_event",
        payload=json.loads(event.json()),
        expected_status=status.HTTP_204_NO_CONTENT,
        return_json=False,
    )


helpers.api_route_create(
    router,
    add_test_events,
    path="/add_event",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test event was added to the database",
        },
        status.HTTP_403_FORBIDDEN: {"description": "Unable to add test event when not running in TESTING mode"},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)


#
# RESET TEST DATABASE
#


def reset_test_database():
    db_api.post(
        path="/test/reset_database", payload=None, expected_status=status.HTTP_204_NO_CONTENT, return_json=False
    )


helpers.api_route_create(
    router,
    reset_test_database,
    path="/reset_database",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test database tables were reset",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Unable to reset the test database when not running in TESTING mode"
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
