import datetime
from uuid import UUID
from fastapi_camelcase import CamelModel
from pydantic import EmailStr


class UserLoginSchema(CamelModel):
    email: EmailStr
    password: str


class UserOutSchema(CamelModel):
    """ Схема без пароля, для просмотра данных """
    email: EmailStr
    id: UUID|None=None
    is_active: bool
    last_login: datetime.datetime|None
    username: str|None
    role: int

    class Config:
        orm_mode=True


class UserSchema(UserLoginSchema, UserOutSchema):
    ...


class SearchUserOut(CamelModel):
    count: int
    users: list[UserOutSchema]


class TokenSchema(CamelModel):
    access_token: str


class PasswordResetSchema(CamelModel):
    email: EmailStr


class PasswordResetTokenSchema(CamelModel):
    token: str
    password: str | None = None
