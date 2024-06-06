from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./wdd.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # by default sqllite allows one thread to communicate with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # we set all the commit, flush to false so that we can have all the control programmatically
Base = declarative_base() # object of the database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()