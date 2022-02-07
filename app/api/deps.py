from models.database import Blockchain
from models.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_blockchain():
    blockchain = Blockchain
    yield blockchain