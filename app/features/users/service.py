from app.features.users.schemas import UserCreate


def list_users() -> list[dict]:
    return []


def get_user(user_id: int) -> dict | None:
    _ = user_id
    return None


def create_user(payload: UserCreate) -> dict:
    return payload.model_dump()
