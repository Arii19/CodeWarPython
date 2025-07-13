import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

DB_PATH = "livros.db"

@st.cache_data
def carregar_dados():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM livros", conn)
    conn.close()
    return df

st.set_page_config(page_title="📚 Dashboard de Livros", layout="wide")
st.title("📘 Dashboard Interativo de Livros")

df = carregar_dados()

# Tabela
with st.expander("📋 Ver Tabela Completa"):
    st.dataframe(df)

# Filtros
col1, col2 = st.columns(2)
with col1:
    autores = df["autor"].dropna().unique().tolist()
    filtro_autor = st.selectbox("Filtrar por Autor:", ["Todos"] + autores)
with col2:
    generos = df["genero"].dropna().unique().tolist()
    filtro_genero = st.selectbox("Filtrar por Gênero:", ["Todos"] + generos)

# Aplica os filtros
if filtro_autor != "Todos":
    df = df[df["autor"] == filtro_autor]

if filtro_genero != "Todos":
    df = df[df["genero"] == filtro_genero]

if not df.empty:
    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Top 20 Autores com Mais Livros")
        df_autores = df["autor"].value_counts().nlargest(20).reset_index()
        df_autores.columns = ["autor", "count"]
        fig1 = px.bar(df_autores, x="autor", y="count",
                      title="Livros por Autor",
                      labels={"autor": "Autor", "count": "Quantidade"},
                      height=500)
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)



fig2 = px.bar(df_generos.sort_values(by="count", ascending=False).head(15),
              x="genero", y="count", title="Top 15 Gêneros",
              labels={"genero": "Gênero", "count": "Quantidade"},
              height=500)
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)


# =========================
# 📄 RELATÓRIO DE GÊNEROS
# =========================
st.markdown("---")
st.header("📄 Relatório de Gêneros Literários")

# Agrupamento por gênero
df_relatorio = df["genero"].value_counts().reset_index()
df_relatorio.columns = ["Gênero", "Quantidade de Livros"]

# Exibição da tabela de relatório
st.dataframe(df_relatorio, use_container_width=True)

# Botão para baixar CSV
csv = df_relatorio.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Baixar Relatório CSV",
    data=csv,
    file_name="relatorio_generos.csv",
    mime="text/csv"
)