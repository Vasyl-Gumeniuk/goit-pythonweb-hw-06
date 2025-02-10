import atexit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(url_to_db)

Session = sessionmaker(bind=engine)
session = Session()


def close_session():
    session.close()


atexit.register(close_session)
