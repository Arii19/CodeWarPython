import os
import pandas as pd
from os.path import join
from datetime import datetime, timedelta
import requests
from database import SessionLocal
from models import Livro

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
                "categories": ", ".join(info.get("categories", []))
            })

        df = pd.DataFrame(livros)
        print("DataFrame extraído:")
        print(df.head())
        return df

    except Exception as e:
        print(f"Erro na extração: {e}")

    
def transform(df):
    # Transforma o DataFrame renomeando colunas e tratando valores nulos
    try:

        df = df.rename(columns={
            "title": "nome",
            "author": "autor",
            "textSnippet": "descricao",
            "categories": "genero"
        })

        df = df.where(pd.notnull(df), None)

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