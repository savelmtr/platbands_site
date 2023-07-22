from sqlalchemy.orm import declarative_base
from sqlalchemy import func, Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False, server_default='False', nullable=False)


class Article(Base):
    __tablename__ = 'articles'

    slug = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
