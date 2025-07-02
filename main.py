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
    Livro(id=3, título='Hábitos Atômicos', autor='James Clear'),
    Livro(id=4, título='1984', autor='George Orwell'),
    Livro(id=5, título='Dom Quixote', autor='Miguel de Cervantes'),
    Livro(id=6, título='O Pequeno Príncipe', autor='Antoine de Saint-Exupéry'),
    Livro(id=7, título='A Revolução dos Bichos', autor='George Orwell'),
    Livro(id=8, título='O Código Da Vinci', autor='Dan Brown'),
    Livro(id=9, título='Moby Dick', autor='Herman Melville'),
    Livro(id=10, título='Crime e Castigo', autor='Fiódor Dostoiévski'),
    Livro(id=11, título='O Alquimista', autor='Paulo Coelho'),
    Livro(id=12, título='A Guerra dos Tronos', autor='George R.R. Martin'),
    Livro(id=13, título='O Morro dos Ventos Uivantes', autor='Emily Brontë'),
    Livro(id=14, título='Cem Anos de Solidão', autor='Gabriel García Márquez'),
    Livro(id=15, título='O Senhor das Moscas', autor='William Golding'),
    Livro(id=16, título='Corte de Espinhos e Rosas', autor='Sarah J. Maas'),
    Livro(id=17, título='Coroa de Meia-Noite', autor='Sarah J. Maas'),
    Livro(id=18, título='Fúria dos Reis', autor='Sarah J. Maas'),
    Livro(id=19, título='Império de Tempestades', autor='Sarah J. Maas'),
    Livro(id=20, título='Rainha das Sombras', autor='Sarah J. Maas'),
    Livro(id=21, título='Crescendo', autor='Sarah J. Maas'),
    Livro(id=22, título='Heir of Fire', autor='Sarah J. Maas'),
    Livro(id=23, título='Queen of Shadows', autor='Sarah J. Maas'),
    Livro(id=24, título='Empire of Storms', autor='Sarah J. Maas'),
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
