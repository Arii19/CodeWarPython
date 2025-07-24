from fastapi.testclient import TestClient
from api.main import app
from datetime import datetime

client = TestClient(app)

def test_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "API da Biblioteca" in response.json()["mensagem"]

def test_criar_livro():
    response = client.post("/livros", json={
        "nome": "O que aprendi com o silêncio",
        "autor": "Monja Coen",
        "descricao": "Monja, jornalista, pensadora. Por trás da figura serena e sempre alegre, existe uma das maiores personalidades brasileiras da atualidade. Suas convicções são precisas e duradouras, mesmo que transmitidas de maneira doce e leve. Seus ensinamentos têm formado uma geração livre de preconceitos religiosos e focada na evolução do eu interior, na liberdade dos pensamentos, no controle do ego e principalmente na possibilidade de ser zen em um mundo caótico. Aqui, Coen Roshi conta sua história com um olhar inusitado. Às vezes emotivo, em outros momentos sarcástico, mas sempre com a capacidade de fazer de um instante o infinito e do infinito um instante. Descubra por que o silêncio foi tão importante em meio a tantas histórias barulhentas e dissonantes.",
        "genero": "Reflexão",
        "capa": "http://books.google.com/books/content?id=-PezDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
    })
    assert response.status_code == 200
    print(response.status_code, response.json())
    assert response.json()["nome"] == "O que aprendi com o silêncio"
    
def test_listar_livros():
    response = client.get("/livros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_livro_por_id():
    id_livro = 155

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
    id_livro = 287
    
    response = client.delete(f"/livros/{id_livro}")
    assert response.status_code == 200
    
    data_exclusao = response.json().get("data_exclusao")
    assert data_exclusao is not None
    assert data_exclusao != ""

