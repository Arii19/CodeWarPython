from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Conexão direta (sem usar variável de ambiente)
SQLALCHEMY_DATABASE_URL = "postgresql://ari:caIN95fnEcr4S7Mk1gkyamxXA4oMwPHj@dpg-d1m5pt63jp1c73ebv31g-a.oregon-postgres.render.com/livros_533j"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
