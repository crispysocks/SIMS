import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        pool_recycle=settings.DB_POOL_RECYCLE,
    )


@pytest.fixture(scope="session")
def engine_url(engine):
    return engine.url


@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()