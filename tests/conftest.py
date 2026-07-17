import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base
from app.database.database import get_db

TEST_DATABASE_URL = "sqlite:///./test_airline.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

    if os.path.exists("test_airline.db"):
        os.remove("test_airline.db")


@pytest.fixture()
def db():

    connection = TestingSessionLocal()

    try:
        yield connection

    finally:
        connection.close()


@pytest.fixture()
def client(db):

    def override_get_db():

        try:
            yield db

        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()