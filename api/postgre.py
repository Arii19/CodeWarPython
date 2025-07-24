import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# postgre.py


Base = declarative_base()

def get_engine():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL não está definida.")
    return create_engine(url)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
