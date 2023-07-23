import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    os.getenv('PG_URI_ASYNC'),
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=5
)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.rollback()
            await session.close()


async def get_session_link() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session.begin() as session:
        return session
