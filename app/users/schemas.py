import datetime
from uuid import UUID
from fastapi_camelcase import CamelModel
from pydantic import EmailStr


class UserLoginSchema(CamelModel):
    email: EmailStr
    password: str


class UserSchema(UserLoginSchema):
    id: UUID|None=None
    is_active: bool
    last_login: datetime.datetime|None
    role: int

    class Config:
        orm_mode=True


class TokenSchema(CamelModel):
    access_token: str


class PasswordResetSchema(CamelModel):
    email: EmailStr


class PasswordResetTokenSchema(CamelModel):
    token: str
    password: str | None = None
