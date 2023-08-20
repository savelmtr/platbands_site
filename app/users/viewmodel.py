import base64
import datetime
from pathlib import Path
from uuid import UUID
from general import settings
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserSchema, PasswordResetTokenSchema
from sqlalchemy.future import select
from general.models import User
from sqlalchemy.dialects.postgresql import insert
from .utils import generate_reset_password_hash, get_hashed_password
from lib.utils import email_backend
from aiofile import async_open
from lib.exceptions import HTTP400
from sqlalchemy import update


class UserModel:
    templates_dir = 'users/templates'
    reset_pass_email_simple_template = 'reset_pass_simple_email_template.txt'

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, email: str|None=None, id_: UUID|None=None) -> UserSchema|None:
        req = select(User).where(User.is_active == True)
        if id_ is not None:
            req = req.where(User.id == id_)
        else:
            req = req.where(User.email == email)
        q = await self.session.execute(req)
        user = q.scalar()
        return UserSchema.from_orm(user) if user else user

    async def create(self, user: UserSchema) -> UserSchema:
        req = (
            insert(User)
            .values(**user.dict())
            .on_conflict_do_nothing(index_elements=['email'])
            .returning(User)
        )
        q = await self.session.execute(req)
        new_user = q.scalar()
        assert new_user is not None, f'Пользователь с email {user.email} уже существует'
        await self.session.commit()
        return UserSchema.from_orm(new_user)
    
    async def update(self, userid: UUID, values: dict):
        req = update(User).where(User.id == userid).values(**values)
        await self.session.execute(req)
        await self.session.commit()
    
    async def apply_template(self, template_name: str, dict_for_template: dict):
        async with async_open(Path(self.templates_dir) / template_name, 'r') as af:
            template = await af.read()
        return template.format(**dict_for_template)

    async def send_reset_pass(self, user: User):
        day = datetime.date.today().toordinal()
        token = generate_reset_password_hash(user, day)
        txt = await self.apply_template(
            self.reset_pass_email_simple_template,
            {
                'base_url': settings.BASE_URL,
                'reset_url': settings.URL_FOR_RESET_PASS,
                'token': token,
                'username': user.email
            }
        )
        await email_backend.send_email(
            user.email, settings.BASE_EMAIL,
            f'Сброс пароля для {settings.BASE_URL}',
            simple_txt=txt
        )

    async def reset_password(self, email: str):
        if (user := await self.get(email=email)) is not None:
            await self.send_reset_pass(user)
            return True
        else:
            return False

    async def check_reset_password_token(self, initial_token: str):
        try:
            id64, day64, token = initial_token.split('-')
            userid = UUID(base64.urlsafe_b64decode(id64).decode())
            day = int(base64.urlsafe_b64decode(day64))
        except Exception as e:
            raise HTTP400(f'Токен не соответствует стандарту: {e}')
        nowday = datetime.date.today().toordinal()
        if abs(nowday - day) > settings.PASSWORD_RESET_TOKEN_MAX_DAYS:
            raise HTTP400('Токен устарел.')
        if (user := await self.get(id_=userid)) is None:
            raise HTTP400('Пользователя не существует.')
        test_token = generate_reset_password_hash(user, day)
        test_hash = test_token.split('-')[-1]
        if test_hash != token:
            raise HTTP400('Неверный токен.')
        return user

    async def reset(self, data: PasswordResetTokenSchema):
        user = await self.check_reset_password_token(data.token)
        new_password = get_hashed_password(data.password)
        await self.update(user.id, {'password': new_password})
