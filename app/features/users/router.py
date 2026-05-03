from fastapi import APIRouter

from app.features.users.schemas import UserCreate
from app.features.users.service import create_user, get_user, list_users

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"module": "users", "status": "ready"}


@router.get("/")
def read_users() -> list[dict]:
    return list_users()


@router.get("/{user_id}")
def read_user(user_id: int) -> dict | None:
    return get_user(user_id)


@router.post("/")
def add_user(payload: UserCreate) -> dict:
    return create_user(payload)
