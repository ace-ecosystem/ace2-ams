import requests

from fastapi import HTTPException, status
from typing import Optional

from core.config import get_settings


def _request(method: str, path: str, expected_status: int, payload: Optional[dict] = None, return_json: bool = False):
    result = requests.request(method=method, url=f"{get_settings().database_api_url}{path}", json=payload)

    if result.status_code not in [
        expected_status,
        status.HTTP_200_OK,
        status.HTTP_201_CREATED,
        status.HTTP_204_NO_CONTENT,
    ]:
        raise HTTPException(status_code=result.status_code, detail=result.text)

    if return_json:
        return result.json()


def get(path: str, expected_status: int = status.HTTP_200_OK, return_json: bool = True):
    return _request(method="GET", path=path, expected_status=expected_status, return_json=return_json)


def patch(path: str, payload: dict, expected_status: int = status.HTTP_204_NO_CONTENT, return_json: bool = False):
    return _request(
        method="PATCH", path=path, expected_status=expected_status, payload=payload, return_json=return_json
    )


def post(path: str, payload: dict, expected_status: int = status.HTTP_201_CREATED, return_json: bool = True):
    return _request(method="POST", path=path, expected_status=expected_status, payload=payload, return_json=return_json)
