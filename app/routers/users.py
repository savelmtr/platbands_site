from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from lib.db import get_session
from lib.viewmodel import UserModel
from lib.schemas import UserLoginSchema, TokenSchema
from lib.utils import verify_password, signJWT
from lib.bearer import JWTBearer
from lib.exceptions import HTTP400, HTTP500, HTTP401

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


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(credentials = Depends(JWTBearer()), session: AsyncSession=Depends(get_session)):
    model = UserModel(session)
    user = await model.get(credentials['user_id'])
    return user
