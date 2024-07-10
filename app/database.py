from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models import Base

DATABASE_URL = "sqlite:///./todo_list"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base.metadata.create_all(engine)

def get_session():
    """Generate the session to connect the database"""
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()