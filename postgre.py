import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = "postgresql://livros_7czp_user:zHwTO6dsT5ZcG5ELalDGxDEweWmyWl84@dpg-d1rg3uqli9vc73b6m5bg-a.oregon-postgres.render.com/livros_7czp"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
