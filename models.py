from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    data_inclusao = Column(DateTime, default=datetime.utcnow)
    data_edicao = Column(DateTime, nullable=True)
    data_exclusao = Column(DateTime, nullable=True)
