import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
st.set_page_config(page_title="📚 Se Dashboard de Livros", layout="wide")

# ========== FUNÇÃO DE EXTRAÇÃO ==========
@st.cache_data
def extract_data():
    url = "https://api-biblioteca-lg6i.onrender.com/livros"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        st.error("Erro ao acessar a API.")
        return pd.DataFrame()

# ========== CARREGAR DADOS ==========
df = extract_data()

if df.empty:
    st.warning("Nenhum dado disponível para exibir.")
    st.stop()

# ========== PRÉ-PROCESSAMENTO ==========
df['data_inclusao'] = pd.to_datetime(df['data_inclusao'])
df['ano_inclusao'] = df['data_inclusao'].dt.year

# ========== SIDEBAR ==========
st.sidebar.title("📊 Filtros")

autores = df['autor'].dropna().unique()
generos = df['genero'].dropna().unique()

autor_sel = st.sidebar.multiselect("Autor", autores, default=autores)
genero_sel = st.sidebar.multiselect("Gênero", generos, default=generos)

df_filtrado = df[
    df['autor'].isin(autor_sel) & 
    df['genero'].isin(genero_sel)
]

# ========== TÍTULO ==========
st.markdown(
    "<h2 style='text-align: center;'>📈 📚 Análise das suas leituras</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>Leituras novas ao longo do lempo</h4>",
    unsafe_allow_html=True
)

# ========== MÉTRICAS ==========
col1, col2, col3 = st.columns(3)
col1.metric("📚 Total de Livros", len(df))
col2.metric("📌 Autores únicos", df['autor'].nunique())
col3.metric("🗂️ Gêneros únicos", df['genero'].nunique())

st.divider()

# ========== GRÁFICO: LIVROS POR GÊNERO ==========

st.markdown(
    "<h3 style='text-align: center;'>📘 Quantidade de Livros lidos por Gênero</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>Livros por Gênero</h4>",
    unsafe_allow_html=True
)
genero_count = df_filtrado['genero'].value_counts().reset_index()
genero_count.columns = ['Gênero', 'Quantidade']

fig_genero = px.bar(
    genero_count,
    x='Gênero',
    y='Quantidade',
    color='Gênero',
    template='plotly_dark',
    text='Quantidade'
)
fig_genero.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_genero, use_container_width=True)

# ========== GRÁFICO DE PIZZA: TOP 10 AUTORES E 10 GENEROS ==========

top_autores = (
    df['autor']
    .value_counts()
    .nlargest(10)
    .reset_index()
)
top_autores.columns = ['autor', 'quantidade']

fig_autores = px.pie(
    top_autores,
    names='autor',
    values='quantidade',
    hole=0.4,
    width=700,
    height=500
)
chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('📚 Seus Top 10 autores mais lidos')
    fig = px.pie(top_autores, values = "autor", names = "quantidade", template = "plotly_dark")
    fig_autores.update_traces(text = top_autores["quantidade"], textposition = "inside")
    st.plotly_chart(fig_autores,use_container_width=True)

top_generos = (
    df['genero']
    .value_counts()
    .nlargest(10)
    .reset_index()
)
top_generos.columns = ['genero', 'quantidade']

fig_generos = px.pie(
    top_generos,
    names='genero',
    values='quantidade',
    hole=0.4,
    width=700,
    height=500
)

with chart2:
    st.subheader('🏆 Seus Top 10 Gêneros mais lidos')
    fig = px.pie(top_generos, values = "genero", names = "quantidade", template = "gridon")
    fig_generos.update_traces(text=top_generos["quantidade"], textposition="inside")
    st.plotly_chart(fig_generos,use_container_width=True)


# ========== GRÁFICO DE BARRAS: TOP 10 AUTORES MAIS CADASTRADOS ==========
st.markdown(
    "<h3 style='text-align: center;'>🏆 Top 10 Autores com Mais Livros Cadastrados</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>Top 10 Autores com Mais Livros</h4>",
    unsafe_allow_html=True
)

top10_autores_totais = (
    df['autor']
    .value_counts()
    .nlargest(10)
    .reset_index()
)
top10_autores_totais.columns = ['autor', 'quantidade']

fig_top10_autores = px.bar(
    top10_autores_totais,
    x='autor',
    y='quantidade',
    color='autor',
    text='quantidade',
    template='plotly_white',
    height=600
)
fig_top10_autores.update_layout(showlegend=False, title_x=0.5)
fig_top10_autores.update_traces(textposition='outside')

col_esq, col_centro, col_dir = st.columns([1, 2, 1])
with col_centro:
    st.plotly_chart(fig_top10_autores, use_container_width=True)

# ========== GRÁFICO: INCLUSÕES POR ANO ==========

st.markdown(
    "<h3 style='text-align: center;'>📈 Evolução da sua leitura</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'>Inclusão de Livros ao Longo do Tempo</h4>",
    unsafe_allow_html=True
)
inclusao_por_ano = df_filtrado.groupby(df_filtrado['data_inclusao'].dt.to_period("M")).size().reset_index(name='Quantidade')
inclusao_por_ano['data_inclusao'] = inclusao_por_ano['data_inclusao'].astype(str)

fig_evolucao = px.line(
    inclusao_por_ano,
    x='data_inclusao',
    y='Quantidade',
    markers=True,
    template='plotly_white'
)
fig_evolucao.update_traces(line=dict(color='green'))
st.plotly_chart(fig_evolucao, use_container_width=True)
