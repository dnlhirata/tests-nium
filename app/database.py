import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL=os.getenv('DB_STRING_CONN')

engine = create_engine(DATABASE_URL)
Base = declarative_base()