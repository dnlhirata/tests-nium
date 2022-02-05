import os

from sqlalchemy import create_engine

DATABASE_URL=os.getenv('DB_STRING_CONN')

engine = create_engine(DATABASE_URL)