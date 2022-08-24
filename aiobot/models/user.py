from sqlalchemy import Column, Integer, String, Boolean

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    telegram_id = Column(Integer, autoincrement=False, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, autoincrement=False)
    ban = Column(Boolean, nullable=False, default=False)
