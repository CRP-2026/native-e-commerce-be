from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password


def authenticate_user(email: str, password: str) -> bool:
    _ = (email, password)
    return False


def build_access_token(subject: str) -> str:
    return create_access_token({"sub": subject}, timedelta(minutes=settings.access_token_expire_minutes))


def get_password_hash(password: str) -> str:
    return hash_password(password)


def check_password(plain_password: str, hashed_password: str) -> bool:
    return verify_password(plain_password, hashed_password)
