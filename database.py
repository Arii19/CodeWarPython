from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Conexão direta (sem usar variável de ambiente)
SQLALCHEMY_DATABASE_URL = "postgresql://ari:caIN95fnEcr4S7Mk1gkyamxXA4oMwPHj@dpg-d1m5pt63jp1c73ebv31g-a.oregon-postgres.render.com/livros_533j"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



DATABASE_URL = "sqlite:///./livros.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()