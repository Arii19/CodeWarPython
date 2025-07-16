import os
import pandas as pd
from os.path import join
from datetime import datetime, timedelta
import requests
from database import SessionLocal
from models import Livro
 from urllib.parse import quote_plus

def extract():
    # Extrai dados da API do Google Books para livros de um autor específico
    try:
        url = ("https://www.googleapis.com/books/v1/volumes?q=inauthor:{autor}&maxResults=40")
        response = requests.get(url)
        if response.status_code != 200:
         raise Exception(f"Erro ao acessar a API: {response.status_code}")
        dados = response.json()
        livros = []

        for item in dados.get('items', []):
            info = item.get('volumeInfo', {})
            livros.append({
                "title": info.get("title"),
                "author": ", ".join(info.get("authors", [])),
                "textSnippet": info.get("description", ""),  
                "categories": ", ".join(info.get("categories", [])),
                "thumbnail": info.get("thumbnail", "")

            })

        df = pd.DataFrame(livros)
        print("DataFrame extraído:")
        print(df.head())
        return df

    except Exception as e:
        print(f"Erro na extração: {e}")

def atualizar_capas():
    session = SessionLocal()
    
    # Buscar livros que não têm capa
    livros_sem_capa = session.query(Livro).filter((Livro.capa == None) | (Livro.capa == "")).all()
    
    for livro in livros_sem_capa:
        titulo = livro.nome
        
        # Escapar caracteres especiais para URL (ex: espaços)
       
        titulo_encoded = quote_plus(titulo)
        
        # Montar URL da API Google Books para buscar pelo título
        url = f"https://www.googleapis.com/books/v1/volumes?q={titulo_encoded}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                items = dados.get("items", [])
                
                if items:
                    volume_info = items[0].get("volumeInfo", {})
                    image_links = volume_info.get("imageLinks", {})
                    capa_url = image_links.get("thumbnail") or image_links.get("smallThumbnail")
                    
                    if capa_url:
                        livro.capa = capa_url
                        print(f"Capa atualizada para '{titulo}': {capa_url}")
                        
            else:
                print(f"Erro ao buscar '{titulo}': status {response.status_code}")
        except Exception as e:
            print(f"Erro na requisição para '{titulo}': {e}")

    session.commit()  # <--- Adicione isso para salvar as alterações!
    session.close()
    
def transform(df):
    # Transforma o DataFrame renomeando colunas, tratando nulos e agrupando gêneros
    try:
        df = df.rename(columns={
            "title": "nome",
            "author": "autor",
            "textSnippet": "descricao",
            "categories": "genero"
        })

        df = df.where(pd.notnull(df), None)

        # Normalização e agrupamento de gêneros
        def classificar_genero(genero):
            if not genero:
                return "Outros"
            genero = str(genero).lower()

            if any(p in genero for p in ["fantasia", "mitologia", "mágico", "magico"]):
                return "Fantasia"
            elif "ficção científica" in genero or "espaço" in genero or "futurista" in genero:
                return "Ficção Científica"
            elif "ficção" in genero or "fantástico" in genero or "distopia" in genero:
                return "Ficção Geral"
            elif "romance" in genero or "amor" in genero or "gótico" in genero or "clássico" in genero or "drama" in genero:
                return "Romance"
            elif "aventura" in genero:
                return "Aventura"
            elif "suspense" in genero or "mistério" in genero or "thriller" in genero or "policial" in genero:
                return "Suspense / Mistério"
            elif "terror" in genero or "horror" in genero:
                return "Terror / Horror"
            elif "histórico" in genero or "história" in genero or "guerra" in genero:
                return "Histórico"
            elif "infantil" in genero or "jovem adulto" in genero or "juvenil" in genero:
                return "Infantil / Juvenil"
            elif "filosófico" in genero or "psicológico" in genero or "reflexão" in genero:
                return "Filosófico / Psicológico"
            elif "religião" in genero or "espiritual" in genero or "fé" in genero:
                return "Religião / Espiritual"
            elif "autoajuda" in genero or "desenvolvimento pessoal" in genero:
                return "Autoajuda / Desenvolvimento Pessoal"
            elif any(p in genero for p in ["educação", "ciência", "tecnologia", "engenharia"]):
                return "Educação / Acadêmico"
            elif "biografia" in genero or "não ficção" in genero or "ensaio" in genero:
                return "Biografia / Não ficção"
            else:
                return "Outros"

        # Criação da nova coluna com o gênero principal
        df["genero_principal"] = df["genero"].apply(classificar_genero)

        print("DataFrame transformado:")
        print(df.head())

        return df

    except Exception as e:
        print(f"Erro na transformação: {e}")
        raise


def load(df):
    # Carrega os dados no banco de dados SQLite
    try:
        session = SessionLocal()
        count_novos = 0

        for _, row in df.iterrows():

            livro_existente = session.query(Livro).filter_by(nome=row["nome"], autor=row["autor"]).first()
            if not livro_existente:
                novo_livro = Livro(
                    nome=row["nome"],
                    autor=row["autor"],
                    descricao=row["descricao"],
                    genero=row["genero"]
                )
                session.add(novo_livro)
                count_novos += 1

        session.commit()
        print(f"Carga concluída com sucesso! Livros inseridos: {count_novos}")
    except Exception as e:
        print(f"Erro na carga: {e}")
        session.rollback()
        raise
    finally:
        session.close()

dados = extract()
dados_tratados = transform(dados)
load(dados_tratados)
atualizar_capas()