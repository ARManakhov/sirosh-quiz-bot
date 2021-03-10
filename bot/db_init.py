import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity import *

db_url = os.environ['DATABASE_URL']

engine = create_engine(db_url, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
default_session = Session()


def get_session():
    return default_session

