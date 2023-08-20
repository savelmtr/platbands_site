from fastapi import APIRouter, Body, Depends
from users.bearer import JWTBearer
from lib.db import get_session
from lib.exceptions import HTTP400, HTTP401
from .schemas import TokenSchema, UserLoginSchema, PasswordResetSchema, PasswordResetTokenSchema
from .utils import signJWT, verify_password
from .viewmodel import UserModel
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["users"])


@router.post('/login', summary="Создаёт access и refresh токены", response_model=TokenSchema)
async def login(
    login_data: UserLoginSchema = Body(),
    session: AsyncSession=Depends(get_session)
) -> TokenSchema:
    model = UserModel(session)
    user = await model.get(login_data.email)
    if user is None:
        raise HTTP401({
            'for': 'email',
            'text': f"Активного пользователя с email {login_data.email} не существует."
        })

    hashed_pass = user.password
    if not verify_password(login_data.password, hashed_pass):
        raise HTTP401({'for': 'password', 'text': "Неверный пароль"})
    
    return signJWT(user.email)


@router.post('/reset-password-req', summary='Запрос сброса пароля')
async def reset_pass(
    data: PasswordResetSchema = Body(),
    session: AsyncSession=Depends(get_session)
) -> None:
    model = UserModel(session)
    res = await model.reset_password(data.email)
    if not res:
        raise HTTP400({
            'for': 'email',
            'text': f"Активного пользователя с email {data.email} не существует."
        })


@router.post('/reset', summary='Сброс пароля')
async def reset_pass(
    data: PasswordResetTokenSchema = Body(),
    session: AsyncSession=Depends(get_session)
) -> None:
    model = UserModel(session)
    if data.password is not None:
        await model.reset(data)
    else:
        await model.check_reset_password_token(data.token)


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(credentials = Depends(JWTBearer()), session: AsyncSession=Depends(get_session)):
    model = UserModel(session)
    user = await model.get(credentials['user_id'])
    return user
