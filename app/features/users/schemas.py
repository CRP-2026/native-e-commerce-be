from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str | None = None
    avatar: str | None = None
    bio: str | None = None
