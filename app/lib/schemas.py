from fastapi_camelcase import CamelModel
from pydantic import EmailStr


class UserLoginSchema(CamelModel):
    email: EmailStr
    password: str


class UserSchema(UserLoginSchema):
    is_active: bool

    class Config:
        orm_mode=True


class TokenSchema(CamelModel):
    access_token: str
