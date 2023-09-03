from users.viewmodel import UserModel
from lib.db import get_session_link
import asyncio
from users.schemas import UserSchema
from users.utils import get_hashed_password
from users.enums import RolesEnum


async def main():
    session = await get_session_link()
    try:
        model = UserModel(session)
        email = input('Введите email:')
        password = input('Введите пароль:')
        await model.create(UserSchema(
            email=email,
            password=password,
            username='Superuser',
            is_active=True,
            role=RolesEnum.SuperUser.value
        ))
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
