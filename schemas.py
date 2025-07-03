from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LivroBase(BaseModel):
    nome: str
    autor: str
    descricao: str 
    genero: str

class LivroCreate(LivroBase):
    pass

class LivroUpdate(LivroBase):
    pass

class LivroResponse(LivroBase):
    id: int
    data_inclusao: datetime
    data_edicao: Optional[datetime]
    data_exclusao: Optional[datetime]

    class Config:
        orm_mode = True
