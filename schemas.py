from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Define os esquemas Pydantic usados na API

# Classe base com os campos comuns dos livros
class LivroBase(BaseModel):
    nome: str
    autor: str
    descricao: str 
    genero: str
    capa: Optional[str] = None  # Capa do livro, opcional

# Esquema para criação de livros (POST)
class LivroCreate(LivroBase):
    pass

# Esquema para atualização de livros (PUT)
class LivroUpdate(LivroBase):
    pass

# Esquema para resposta da API, com campos extras do banco
class LivroResponse(LivroBase):
    id: int
    data_inclusao: datetime
    data_edicao: Optional[datetime]
    data_exclusao: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

