from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_admin_user, get_store_id
from app.db.models import User as UserRow
from app.features.users import service as users_svc
from app.features.users.schemas import AdminUserActiveIn, UserOut

router = APIRouter()


@router.patch("/users/{user_id}/status", response_model=UserOut)
def patch_user_active_status(
    user_id: str,
    payload: AdminUserActiveIn,
    db: Session = Depends(get_db),
    store_id: Annotated[int, Depends(get_store_id)] = 1,
    admin: UserRow = Depends(get_admin_user),
) -> UserOut:
    row = users_svc.admin_set_user_active(
        db,
        store_id,
        user_id,
        is_active=payload.is_active,
        actor_user_id=admin.id,
    )
    return UserOut(
        id=row.id,
        name=row.name,
        email=row.email,
        phone=row.phone,
        avatar=row.avatar,
        bio=row.bio,
        is_active=row.is_active,
        role=str(row.role),
    )
