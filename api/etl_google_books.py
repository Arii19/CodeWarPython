import pandas as pd
from os.path import join
from datetime import datetime, timezone
import requests
from api.postgre import SessionLocal
from api.models import Livro
from urllib.parse import quote_plus
from sqlalchemy import func

def extract():
    # Extrai dados da API do Google Books para livros de um autor específico
    try:
        url = ("https://www.googleapis.com/books/v1/volumes?q=bestseller&maxResults=40")
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
                        # Corrige o protocolo http para https, se necessário
                        capa_url = capa_url.replace("http://", "https://")
                        livro.capa = capa_url
                        print(f"Capa atualizada para '{titulo}': {capa_url}")
                else:
                    print(f"Nenhuma capa encontrada para '{titulo}'.")
            else:
                print(f"Erro ao buscar '{titulo}': status {response.status_code}")
        except Exception as e:
            print(f"Erro na requisição para '{titulo}': {e}")

    session.commit()  # Salva as alterações no banco
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

        df["nome"] = df["nome"].str.strip().str.title()
        df["autor"] = df["autor"].str.strip().str.title()
       
        df = df.drop_duplicates(subset=["nome"], keep="first").reset_index(drop=True)

        print("DataFrame transformado e com duplicados removidos:")
        print(df.head())

        return df

    except Exception as e:
        print(f"Erro na transformação: {e}")
        raise

def load(df):
    session = SessionLocal()
    try:
        count_novos = 0

        # Inserção de novos livros sem duplicar 
        for _, row in df.iterrows():
            livro_existente = session.query(Livro).filter_by(nome=row["nome"], autor=row["autor"]).first()

            if not livro_existente:
                novo_livro = Livro(
                    nome=row["nome"],
                    autor=row["autor"],
                    descricao=row["descricao"] or "",
                    genero=row["genero"] or "",
                    capa=row.get("thumbnail", "") or "",
                    data_inclusao=datetime.now(timezone.utc)
                )
                session.add(novo_livro)
                count_novos += 1

        session.commit()
        print(f"Carga concluída com sucesso! Livros inseridos: {count_novos}")

        # Remoção de duplicatas antigas 
        subquery = (
            session.query(func.min(Livro.id).label("id"))
            .group_by(Livro.nome, Livro.autor)
            .subquery()
        )

        duplicatas = (
            session.query(Livro)
            .filter(Livro.id.not_in(session.query(subquery.c.id)))
            .all()
        )

        print(f"Total de duplicatas encontradas: {len(duplicatas)}")
        for livro in duplicatas:
            print(f"Removendo duplicado: {livro.nome} - {livro.autor}")
            session.delete(livro)

        session.commit()
        print("Livros duplicados removidos com sucesso!")

        # Atualização de capas dos livros que ainda estão sem 
        livros_sem_capa = session.query(Livro).filter((Livro.capa == None) | (Livro.capa == "")).all()

        for livro in livros_sem_capa:
            titulo_encoded = quote_plus(livro.nome)
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
                            capa_url = capa_url.replace("http://", "https://")
                            livro.capa = capa_url
                            print(f"Capa atualizada para '{livro.nome}': {capa_url}")
                    else:
                        print(f"Nenhuma capa encontrada para '{livro.nome}'.")
                else:
                    print(f"Erro ao buscar '{livro.nome}': status {response.status_code}")
            except Exception as e:
                print(f"Erro na requisição para '{livro.nome}': {e}")

        session.commit()
        print("Capas atualizadas com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"Erro geral durante carga ou atualização de capas: {e}")
        raise

    finally:
        session.close()



dados = extract()
dados_tratados = transform(dados)
load(dados_tratados)
atualizar_capas()
