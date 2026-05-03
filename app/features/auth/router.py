from fastapi import APIRouter

from app.features.auth.schemas import LoginRequest, Token
from app.features.auth.service import build_access_token

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"module": "auth", "status": "ready"}


@router.post("/login", response_model=Token)
def login(payload: LoginRequest) -> Token:
    _ = payload
    return Token(access_token=build_access_token("demo-user"))
