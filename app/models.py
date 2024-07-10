from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    """The class to map the user table"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(128))

class Task(Base):
    """The class to map the task table"""
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(512))
    completed: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))