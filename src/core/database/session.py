from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Write DB Session
SQLALCHEMY_DATABASE_WRITE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT_WRITE}/{settings.DB_NAME}"
)

# Read DB Session
SQLALCHEMY_DATABASE_READ_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT_READ}/{settings.DB_NAME}"
)

engine_write = create_engine(SQLALCHEMY_DATABASE_WRITE_URL, pool_pre_ping=True)
engine_read = create_engine(SQLALCHEMY_DATABASE_READ_URL, pool_pre_ping=True)

SessionLocalWrite = sessionmaker(autocommit=False, autoflush=False, bind=engine_write)
SessionLocalRead = sessionmaker(autocommit=False, autoflush=False, bind=engine_read)


def get_write_db():
    db = SessionLocalWrite()
    try:
        yield db
    finally:
        db.close()


def get_read_db():
    db = SessionLocalRead()
    try:
        yield db
    finally:
        db.close()
