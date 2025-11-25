from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import settings

engine_write = create_engine(settings.SQLALCHEMY_DATABASE_WRITE_URL, pool_pre_ping=True)
engine_read = create_engine(settings.SQLALCHEMY_DATABASE_READ_URL, pool_pre_ping=True)

session_local_write = sessionmaker(autocommit=False, autoflush=False, bind=engine_write)
session_local_read = sessionmaker(autocommit=False, autoflush=False, bind=engine_read)


class Base(DeclarativeBase):
    pass


def get_write_db():
    """Write DB Session"""
    db = session_local_write()
    try:
        yield db
    finally:
        db.close()


def get_read_db():
    """Read DB Session"""
    db = session_local_read()
    try:
        yield db
    finally:
        db.close()
