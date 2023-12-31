import datetime
from uuid import UUID

from fastapi import APIRouter, Body, Depends
from lib.db import get_session
from lib.exceptions import HTTP400, HTTP401
from sqlalchemy.ext.asyncio import AsyncSession

from .enums import RolesEnum
from .schemas import (PasswordResetSchema, PasswordResetTokenSchema, SearchUserOut,
                      TokenSchema, UserLoginSchema, UserOutSchema, UserSchema)
from .utils import signJWT, verify_password
from .viewmodel import RoleKeeper, UserModel


router = APIRouter(prefix="/users", tags=["users"])


@router.get('/admin_test', summary='Get details of currently logged in user')
async def test_token(
    credentials = Depends(RoleKeeper([RolesEnum.SuperUser, RolesEnum.Admin, RolesEnum.Moderator]))
):
    return {'result': True}


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
    
    await model.update(user.id, {
        'last_login': datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    })
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
async def reset_(
    data: PasswordResetTokenSchema = Body(),
    session: AsyncSession=Depends(get_session)
) -> None:
    model = UserModel(session)
    if data.password is not None:
        await model.reset(data)
    else:
        await model.check_reset_password_token(data.token)


@router.get('/', summary='Users list')
async def list_users(
    query: str='',
    page: int=1,
    credentials = Depends(RoleKeeper([RolesEnum.SuperUser])),
    session: AsyncSession=Depends(get_session)
) -> SearchUserOut:
    model = UserModel(session)
    return await model.search(q=query, page=page)


@router.get('/{id_}', summary='Users list')
async def get_user(
    id_: UUID,
    credentials = Depends(RoleKeeper([RolesEnum.SuperUser])),
    session: AsyncSession=Depends(get_session)
) -> UserOutSchema|None:
    model = UserModel(session)
    user = await model.get(id_=id_)
    return UserOutSchema(**user.dict()) if user else user


@router.post('/', summary='Create user')
async def create_user(
    body: UserSchema = Body(...),
    credentials = Depends(RoleKeeper([RolesEnum.SuperUser])),
    session: AsyncSession=Depends(get_session)
) -> UserSchema:
    model = UserModel(session)
    return await model.create(body)


@router.patch('/', summary='Update user')
async def update_user(
    body: UserSchema = Body(...),
    credentials = Depends(RoleKeeper([RolesEnum.SuperUser])),
    session: AsyncSession=Depends(get_session)
) -> UserSchema:
    model = UserModel(session)
    id_ = body.id
    if not id_:
        raise HTTP400('Для обновления данных пользователя необходим id')
    values = body.dict()
    del values['id']
    return await model.update(id_, values)


