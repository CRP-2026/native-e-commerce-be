from __future__ import annotations

import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User


def register_user(db: Session, store_id: int, email: str, password: str, name: str) -> User:
    exists = db.execute(
        select(User).where(User.store_id == store_id, User.email == email, User.deleted_at.is_(None))
    ).scalar_one_or_none()
    if exists:
        raise AppError("conflict", "Email already registered for this store", status_code=409)
    uid = str(uuid.uuid4())
    u = User(
        id=uid,
        store_id=store_id,
        email=email,
        password_hash=hash_password(password),
        name=name,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def login_user(db: Session, store_id: int, email: str, password: str) -> User:
    u = db.execute(
        select(User).where(
            User.store_id == store_id,
            User.email == email,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if u is None or not u.password_hash or not verify_password(password, u.password_hash):
        raise AppError("unauthorized", "Invalid email or password", status_code=401)
    return u


def issue_token(user_id: str, store_id: int) -> str:
    return create_access_token(
        {"sub": user_id, "sid": store_id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
