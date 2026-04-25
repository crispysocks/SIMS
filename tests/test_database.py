import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from sqlalchemy import text


class TestDatabaseConnection:
    def test_mysql_version(self, engine):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            assert version.startswith("8.0"), f"Expected MySQL 8.x, got {version}"

    def test_database_exists(self, engine):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            assert db_name == "student_management"

    def test_session_query(self, db_session):
        result = db_session.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()[0]
        assert db_name == "student_management"

    def test_connection_pool_size(self, engine):
        pool = engine.pool
        assert pool.size() == 5

    def test_engine_url(self, engine_url):
        assert "mysql+pymysql" in str(engine_url)
        assert "student_management" in str(engine_url)