import pandas as pd
from os.path import join
from datetime import datetime, timezone
import requests
from api.postgre import SessionLocal
from api.models import Livro
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

        # Normalização e agrupamento de gêneros

        # REMOÇÃO DE DUPLICADOS: manter apenas a primeira ocorrência de cada nome
        df = df.drop_duplicates(subset=["nome"], keep="first").reset_index(drop=True)

        print("DataFrame transformado e com duplicados removidos:")
        print(df.head())

        return df

    except Exception as e:
        print(f"Erro na transformação: {e}")
        raise


def load(df):
    try:
        session = SessionLocal()
        count_novos = 0

        for _, row in df.iterrows():
            # Verifica se o livro já existe no banco (nome + autor)
            livro_existente = session.query(Livro).filter_by(nome=row["nome"], autor=row["autor"]).first()
            
            if not livro_existente:
                novo_livro = Livro(
                    nome=row["nome"],
                    autor=row["autor"],
                    descricao=row["descricao"] or "",  # caso seja None, evitar erro
                    genero=row["genero"] or "",  # caso seja None, evitar erro
                    capa=row.get("thumbnail", "") or "",  # Caso venha capa no dataframe, se não, vazio
                    data_inclusao=datetime.now(timezone.utc)
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