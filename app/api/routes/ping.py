from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
def ping() -> dict:
    return {"ping": "pong"}
