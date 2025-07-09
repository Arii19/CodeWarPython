from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "API da Biblioteca" in response.json()["mensagem"]

def test_criar_livro():
    response = client.post("/livros", json={
        "nome": "Livro Teste",
        "autor": "Autor Teste",
        "descricao": "Descrição do livro teste",
        "genero": "Ficção"
    })
    assert response.status_code == 200
    print(response.status_code, response.json())
    assert response.json()["nome"] == "Livro Teste"
    
def test_listar_livros():
    response = client.get("/livros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_livro_por_id():
    # cria um novo livro primeiro
    post = client.post("/livros", json={
        "nome": "Livro ID",
        "autor": "Autor ID",
        "descricao": "Descrição do livro teste",
        "genero": "Ficção"
    })
    id_livro = post.json()["id"]
    response = client.get(f"/livros/{id_livro}")
    assert response.status_code == 200
    assert response.json()["id"] == id_livro

def test_atualizar_livro():
    post = client.post("/livros", json={
        "nome": "Livro Antigo",
        "autor": "Autor Antigo",
        "descricao": "Descrição do livro teste",
        "genero": "ficção"
    })
    id_livro = post.json()["id"]
    response = client.put(f"/livros/{id_livro}", json={
        "nome": "Livro Atualizado",
        "autor": "Autor Atualizado",
        "descricao": "Descrição do livro teste, atualizado",
        "genero": "aventura"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Livro Atualizado"

def test_deletar_livro():
    post = client.post("/livros", json={
        "nome": "Livro para Deletar",
        "autor": "Autor Del",
        "descricao": "Descrição do livro teste, deletado",
        "genero": "aventura"
    })
    id_livro = post.json()["id"]
    response = client.delete(f"/livros/{id_livro}")
    assert response.status_code == 200
    assert response.json()["data_exclusao"] is not None