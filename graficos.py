import requests
import pandas as pd
import streamlit as st
import plotly.express as px

BASE_URL = "https://api-biblioteca-lg6i.onrender.com/livros"

def extract():
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a API: {response.status_code}")
        
        dados = response.json()
        
        if not dados:
            print("Nenhum dado encontrado na API.")
            return pd.DataFrame()
        
        df = pd.DataFrame(dados)
        print("DataFrame extraído:")
        print(df.head())
        
        return df

    except Exception as e:
        print(f"Erro na extração: {e}")
        return pd.DataFrame()

# --- Configurações Streamlit ---
st.set_page_config(layout="wide", page_title="Dashboard de Livros")

# Centraliza o título usando HTML
st.markdown("<h1 style='text-align: center; color: #007bff;'>📚 Dashboard de Livros</h1>", unsafe_allow_html=True)

# --- Extração de Dados ---
df = extract()

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a API.")
else:
    # --- Sidebar com Filtros ---
    st.sidebar.header("Filtros")

    # Filtro por Gênero
    todos_generos = ['Todos'] + sorted(df['genero'].unique().tolist())
    genero_selecionado = st.sidebar.selectbox("Filtrar por Gênero:", todos_generos)

    # Filtro por Autor
    todos_autores = ['Todos'] + sorted(df['autor'].unique().tolist())
    autor_selecionado = st.sidebar.selectbox("Filtrar por Autor:", todos_autores)

    # Filtro por Título (Adicionando um filtro de busca por texto)
    busca_titulo = st.sidebar.text_input("Buscar por Título do Livro:", "").lower()

    df_filtrado = df.copy()

    if genero_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['genero'] == genero_selecionado]
    
    if autor_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['autor'] == autor_selecionado]

    if busca_titulo: # Aplica o filtro de título se a busca não estiver vazia
        df_filtrado = df_filtrado[df_filtrado['nome'].str.lower().str.contains(busca_titulo)]

    if df_filtrado.empty:
        st.warning("Nenhum livro encontrado para os filtros selecionados.")
    else:
        # --- Cálculo das Contagens (com base nos dados filtrados) ---
        contagem_autores = df_filtrado['autor'].value_counts().reset_index()
        contagem_autores.columns = ['autor', 'quantidade_de_livros']
        top_autores = contagem_autores.head(10)

        contagem_generos = df_filtrado['genero'].value_counts().reset_index()
        contagem_generos.columns = ['genero', 'quantidade_de_genero']
        top_generos = contagem_generos.head(10)

        # --- Layout das Colunas para Gráficos ---
        col1, col_espaco, col2 = st.columns([8, 1, 8])

        # --- Gráfico de Autores ---
        with col1:
            st.subheader("Autores com Mais Livros Cadastrados")
            fig1 = px.bar(
                top_autores,
                x='autor',
                y='quantidade_de_livros',
                text='quantidade_de_livros',
                color='autor',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                height=500,
                template='seaborn',
                labels={'autor': 'Nome do Autor', 'quantidade_de_livros': 'Número de Livros'},
                title='Top 10 Autores'
            )
            fig1.update_traces(textfont_size=12, textangle=0, textposition="outside")
            fig1.update_layout(showlegend=False)
            fig1.update_xaxes(tickangle=45)
            st.plotly_chart(fig1, use_container_width=True)

        # --- Gráfico de Gêneros ---
        with col2:
            st.subheader("Gêneros Mais Cadastrados")
            fig2 = px.bar(
                top_generos,
                x='genero',
                y='quantidade_de_genero',
                text='quantidade_de_genero',
                color='genero',
                color_discrete_sequence=px.colors.qualitative.D3,
                height=500,
                template='seaborn',
                labels={'genero': 'Gênero do Livro', 'quantidade_de_genero': 'Número de Livros'},
                title='Top 10 Gêneros'
            )
            fig2.update_traces(textfont_size=12, textangle=0, textposition="outside")
            fig2.update_layout(showlegend=False)
            fig2.update_xaxes(tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)

        # --- Tabela de Livros Filtrados ---
        st.subheader("Livros Correspondentes aos Filtros")

        # Seleciona apenas as colunas que você quer exibir na tabela
        # Você pode ajustar isso para mostrar apenas 'titulo', 'autor', 'genero'
        colunas_para_tabela =  colunas_para_tabela = ['nome', 'genero']  # Adicione outras colunas se desejar

        if not df_filtrado.empty:
            # Garante que as colunas existem antes de exibi-las
            df_tabela = df_filtrado[df_filtrado.columns.intersection(colunas_para_tabela)]
            st.dataframe(df_tabela, use_container_width=True)
        else:
            st.info("Nenhum livro corresponde aos filtros aplicados.")