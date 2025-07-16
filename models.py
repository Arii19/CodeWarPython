from sqlalchemy import Column, DateTime, Integer, String, Text
from datetime import datetime, timezone
from database import Base

class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    genero = Column(String(255), nullable=False)
    capa = Column(String(500), nullable=True)
    
    data_inclusao = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data_edicao = Column(DateTime(timezone=True), nullable=True)
    data_exclusao = Column(DateTime(timezone=True), nullable=True)

