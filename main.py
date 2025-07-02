from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# Modelo do livro com validação
class Livro(BaseModel):
    id: int
    título: str
    autor: str

# Lista de livros (simula um "banco de dados" em memória)
livros: List[Livro] = [
    Livro(id=1, título='O Senhor dos Anéis - A Sociedade do Anel', autor='J.R.R Tolkien'),
    Livro(id=2, título='Harry Potter e a Pedra Filosofal', autor='J.K Howling'),
    Livro(id=3, título='James Clear', autor='Hábitos Atômicos'),
]

# Consultar todos os livros
@app.get("/livros", response_model=List[Livro])
def obter_livros():
    return livros

# Consultar livro por ID
@app.get("/livros/{id}", response_model=Livro)
def obter_livro_por_id(id: int):
    for livro in livros:
        if livro.id == id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Criar novo livro
@app.post("/livros", response_model=List[Livro])
def incluir_novo_livro(novo_livro: Livro):
    livros.append(novo_livro)
    return livros

# Editar livro por ID
@app.put("/livros/{id}", response_model=Livro)
def editar_livro_por_id(id: int, livro_alterado: Livro):
    for indice, livro in enumerate(livros):
        if livro.id == id:
            livros[indice] = livro_alterado
            return livros[indice]
    raise HTTPException(status_code=404, detail="Livro não encontrado")

# Excluir livro por ID
@app.delete("/livros/{id}", response_model=List[Livro])
def excluir_livro(id: int):
    for indice, livro in enumerate(livros):
        if livro.id == id:
            del livros[indice]
            return livros
    raise HTTPException(status_code=404, detail="Livro não encontrado")
