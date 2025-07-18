# API de Livros com FastAPI

# 📚 API de Biblioteca - FastAPI

Uma API RESTful simples para gerenciamento de livros, desenvolvida com [FastAPI](https://fastapi.tiangolo.com/), com suporte a criação, leitura, atualização, exclusão lógica e buscas por nome ou autor.

Para acessar: https://api-biblioteca-lg6i.onrender.com

Para acessar: https://diariodeleitura.streamlit.app/
---

## 🚀 Funcionalidades

- ✅ Criar livro (`POST /livros`)
- 📖 Listar livros (`GET /livros`)
- 🔍 Buscar livro por ID (`GET /livros/{id}`)
- 🔎 Buscar livros por nome (`GET /livros/nome/{nome}`)
- 🔎 Buscar livros por autor (`GET /livros/autor/{autor}`)
- 📝 Atualizar livro (`PUT /livros/{id}`)
- ❌ Excluir logicamente (`DELETE /livros/{id}`)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite (ou PostgreSQL, para produção)
- Pydantic
- Uvicorn
- Pytest
- TestClient

---

## 📦 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/Arii19/CodeWarPython.git

