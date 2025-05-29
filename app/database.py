
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)