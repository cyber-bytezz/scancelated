# load env
from dotenv import load_dotenv
load_dotenv(override=True)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_URL = os.getenv('DATABASE_URL')
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine,expire_on_commit=False)
db_session = Session

def get_session():
    session = SessionLocal(bind=engine)
    try:
        yield session
    finally:
        session.close()






