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
        "nome": "Um reino de carne e fogo",
        "autor": "Jennifer L. Armentrout",
        "descricao": "Sangue e Cinzas é um romance arrebatador e impossível de parar de ler.",
        "genero": "Fantasia contemporânea"
    })
    assert response.status_code == 200
    print(response.status_code, response.json())
    assert response.json()["nome"] == "Um reino de carne e fogo"
    
def test_listar_livros():
    response = client.get("/livros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_livro_por_id():
    id_livro = 17

    response = client.get(f"/livros/{id_livro}")
    
    assert response.status_code == 200
    assert response.json()["id"] == id_livro

def test_atualizar_livro():
    id_livro = 65
    
    response = client.put(f"/livros/{id_livro}", json={
        "nome": "A Garota no Trem",
        "autor": "Hawkins Paula ",
        "descricao": "Um thriller psicológico cheio de reviravoltas",
        "genero": "Mistério"
    })
    
    assert response.status_code == 200
    assert response.json()["nome"] == "A Garota no Trem"

def test_deletar_livro():
    id_livro = 195
    
    response = client.delete(f"/livros/{id_livro}")
    assert response.status_code == 200
    
    data_exclusao = response.json().get("data_exclusao")
    assert data_exclusao is not None
    assert data_exclusao != ""