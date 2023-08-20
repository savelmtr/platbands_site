from sqlalchemy.orm import declarative_base
from sqlalchemy import func, Column, String, Boolean, DateTime, Text, text, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from uuid import uuid4


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), default=uuid4, primary_key=True)    
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False, server_default='False', nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    role = Column(Integer, server_default=text('0'), default=0, nullable=False)


# class Article(Base):
#     __tablename__ = 'articles'

#     slug = Column(String, primary_key=True)
#     title = Column(String, nullable=False)
#     content = Column(Text)
#     created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
