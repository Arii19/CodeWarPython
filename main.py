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


# Endpoint raiz para dar boas-vindas e instruções básicas de uso
@app.get("/")
def raiz():
    return {"mensagem": "🚀 API da Biblioteca está no ar! Seja bem-vindo(a)!, "
    "Você pode acessar os endpoints para gerenciar livros."
    "\n Basta colocar a plavra livros no final da URL, por exemplo: /livros"
    "\nMas se você quiser pesquisar por id, basta colocar o id do livro no final da URL, por exemplo: /livros/1"}


# Dependência abre e fecha uma sessão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # garante que a conexão seja encerrada


# Endpoint GET que retorna todos os livros não excluídos logicamente
@app.get("/livros", response_model=List[schemas.LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(models.Livro).filter(models.Livro.data_exclusao == None).all()

# Retorna um livro específico pelo ID, se não estiver excluído
@app.get("/livros/{id}", response_model=schemas.LivroResponse)
def obter_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id, models.Livro.data_exclusao == None).first()
    if not livro:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    return livro

#Busca livros pelo nome do livro ou parte dele
@app.get("/livros/nome/{nome}", response_model=List[schemas.LivroResponse])
def obter_livros_por_nome(nome: str, db: Session = Depends(get_db)):
    livros = db.query(models.Livro).filter(
        models.Livro.nome.ilike(f"%{nome}%"),
        models.Livro.data_exclusao == None
    ).all()
    if not livros:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado com esse nome")
    return livros

#Busca livros pelo autor ou parte do nome do autor
@app.get("/livros/autor/{autor}", response_model=List[schemas.LivroResponse])
def obter_livros_por_autor(autor: str, db: Session = Depends(get_db)):
    livros = db.query(models.Livro).filter(
        models.Livro.autor.ilike(f"%{autor}%"),
        models.Livro.data_exclusao == None
    ).all()
    if not livros:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado para esse autor")
    return livros

# Endpoint POST para criar um novo livro
@app.post("/livros", response_model=schemas.LivroResponse)
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    novo_livro = models.Livro(**livro.dict())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro

# Endpoint PUT para atualizar um livro existente 
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

# Endpoint DELETE que faz exclusão lógica de um livro (marca a data de exclusão)
@app.delete("/livros/{id}", response_model=schemas.LivroResponse)
def deletar_livro(id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id, models.Livro.data_exclusao == None).first()
    if not livro:
        raise HTTPException(status_code=400, detail="Livro não encontrado")
    livro.data_exclusao = datetime.utcnow()
    db.commit()
    return livro
