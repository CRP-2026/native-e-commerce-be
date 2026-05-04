from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.db.models import User as UserRow
from app.features.users.schemas import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_me(current: UserRow = Depends(get_current_user)) -> UserOut:
    return UserOut(
        id=current.id,
        name=current.name,
        email=current.email,
        phone=current.phone,
        avatar=current.avatar,
        bio=current.bio,
    )
