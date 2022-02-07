import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from api.deps import get_blockchain, get_db
from app.main import app
from blockchain.blockchain import Block
from blockchain.blockchain import Blockchain
from models.database import Base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingBlockchain = Blockchain()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_blockchain():
    yield TestingBlockchain


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_blockchain] = override_get_blockchain


@pytest.fixture(scope='session')
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='session')
def blockchain() -> Generator:
    yield TestingBlockchain