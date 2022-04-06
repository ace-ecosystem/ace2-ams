import requests

from fastapi import HTTPException
from typing import Optional

from core.config import get_settings


def _request(method: str, path: str, expected_status: int, payload: Optional[dict] = None):
    result = requests.request(method=method, url=f"{get_settings().database_api_url}{path}", json=payload)

    if result.status_code != expected_status:
        raise HTTPException(status_code=result.status_code, detail=result.text)

    return result.json()


def delete(path: str, expected_status: int):
    return _request(method="DELETE", path=path, expected_status=expected_status)


def get(path: str, expected_status: int):
    return _request(method="GET", path=path, expected_status=expected_status)


def patch(path: str, payload: dict, expected_status: int):
    return _request(method="PATCH", path=path, expected_status=expected_status, payload=payload)


def post(path: str, payload: dict, expected_status: int):
    return _request(method="POST", path=path, expected_status=expected_status, payload=payload)
