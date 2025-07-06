from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models
import schemas
from datetime import datetime
from database import engine
from models import Base

app = FastAPI()

# Criar tabelas no banco
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def raiz():
    return {"mensagem": "🚀 API da Biblioteca está no ar! Seja bem-vindo(a)!, "
    "Você pode acessar os endpoints para gerenciar livros."
    "\n Basta colocar a plavra livros no final da URL, por exemplo: /livros"
    "\nMas se você quiser pesquisar por id, basta colocar o id do livro no final da URL, por exemplo: /livros/1"}


# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros", response_model=List[schemas.LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(models.Livro).filter(models.Livro.data_exclusao == None).all()

@app.get("/livros/{id}", response_model=schemas.LivroResponse)
def obter_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id, models.Livro.data_exclusao == None).first()
    if not livro:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    return livro

@app.get("/livros/autor/{autor}", response_model=List[schemas.LivroResponse])
def obter_livros_por_autor(autor: str, db: Session = Depends(get_db)):
    livros = db.query(models.Livro).filter(
        models.Livro.autor.ilike(f"%{autor}%"),
        models.Livro.data_exclusao == None
    ).all()
    if not livros:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado para esse autor")
    return livros

@app.post("/livros", response_model=schemas.LivroResponse)
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    novo_livro = models.Livro(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

@app.put("/livros/{id}", response_model=schemas.LivroResponse)
def atualizar_livro(id: int, livro: schemas.LivroUpdate, db: Session = Depends(get_db)):
    livro_db = db.query(models.Livro).filter(models.Livro.id == id, models.Livro.data_exclusao == None).first()
    if not livro_db:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    
    for campo, valor in livro.dict().items():
        setattr(livro_db, campo, valor)
    livro_db.data_edicao = datetime.utcnow()
    db.commit()
    db.refresh(livro_db)
    return livro_db

@app.delete("/livros/{id}", response_model=schemas.LivroResponse)
def deletar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id, models.Livro.data_exclusao == None).first()
    if not livro:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    livro.data_exclusao = datetime.utcnow()
    db.commit()
    return livro
