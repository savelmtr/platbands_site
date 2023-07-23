from sqlalchemy.ext.asyncio import AsyncSession
from lib.schemas import UserSchema
from sqlalchemy.future import select
from models import User
from sqlalchemy.dialects.postgresql import insert


class UserModel:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, email: str) -> UserSchema|None:
        req = select(User).where(User.email == email, User.is_active == True)
        q = await self.session.execute(req)
        user = q.scalar()
        print(user)
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
