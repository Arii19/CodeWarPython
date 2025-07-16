import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO

BASE_URL = "https://api-biblioteca-lg6i.onrender.com/livros"

def extract():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        dados = response.json()
        return pd.DataFrame(dados) if dados else pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao acessar a API: {e}")
        return pd.DataFrame()

# Função para exportar dados para Excel
def gerar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Livros", index=False)
    output.seek(0)
    return output

# --- Configurações da Página ---
st.set_page_config(layout="wide", page_title="📚 Dashboard de Livros")

# --- Estilo Customizado ---
st.markdown("""
    <style>
        .main {
            background-color: #121212;
        }
        .stDataFrame div {
            font-size: 16px;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>📚 Dashboard de Livros</h1>", unsafe_allow_html=True)

# --- Tema ---
tema = st.sidebar.radio("🎨 Escolha o Tema", ["Escuro", "Claro"])

if tema == "Claro":
    template_plotly = "plotly_white"
else:
    template_plotly = "plotly_dark"

# --- Extração de Dados ---
df = extract()

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a API.")
else:
    st.sidebar.header("🔍 Filtros")
    st.sidebar.divider()

    if st.sidebar.button("🔄 Limpar Filtros"):
        st.experimental_rerun()

    genero_opcoes = ['Todos'] + sorted(df['genero'].unique())
    genero = st.sidebar.selectbox("Filtrar por Gênero:", genero_opcoes)

    autor_opcoes = ['Todos'] + sorted(df['autor'].unique())
    autor = st.sidebar.selectbox("Filtrar por Autor:", autor_opcoes)

    titulo = st.sidebar.text_input("Buscar por Título do Livro:")

    # --- Filtros ---
    df_filtrado = df.copy()

    if genero != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['genero'] == genero]
    if autor != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['autor'] == autor]
    if titulo:
        df_filtrado = df_filtrado[df_filtrado['nome'].str.lower().str.contains(titulo.lower())]

    if df_filtrado.empty:
        st.warning("Nenhum livro encontrado para os filtros selecionados.")
    else:
        # --- Contagens ---
        top_autores = df_filtrado['autor'].value_counts().head(10).reset_index()
        top_autores.columns = ['autor', 'quantidade_de_livros']

        top_generos = df_filtrado['genero'].value_counts().head(10).reset_index()
        top_generos.columns = ['genero', 'quantidade_de_genero']

        # --- Gráficos ---
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.subheader("👩‍💻 Autores com Mais Livros")
            fig1 = px.bar(
                top_autores,
                x='autor',
                y='quantidade_de_livros',
                text='quantidade_de_livros',
                color='autor',
                color_discrete_sequence=px.colors.qualitative.Vivid,
                height=450,
                template=template_plotly,
                title='Top 10 Autores'
            )
            fig1.update_traces(textposition="outside")
            fig1.update_layout(showlegend=False, margin=dict(t=40))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("📚 Gêneros Mais Cadastrados")
            fig2 = px.bar(
                top_generos,
                x='genero',
                y='quantidade_de_genero',
                text='quantidade_de_genero',
                color='genero',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                height=450,
                template=template_plotly,
                title='Top 10 Gêneros'
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(showlegend=False, margin=dict(t=40))
            st.plotly_chart(fig2, use_container_width=True)

        # --- Tabela e Exportação ---
        st.markdown("### 📖 Livros Correspondentes aos Filtros")
        colunas_para_exibir = ['nome', 'autor', 'genero']
        st.dataframe(df_filtrado[colunas_para_exibir], use_container_width=True, height=400)

                # --- Capas e Descrições dos Livros ---
        st.markdown("### 🖼️ Capas e Descrições dos Livros Filtrados")

        for _, row in df_filtrado.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if pd.notna(row.get('capa')) and row['capa']:
                        st.image(row['capa'], use_column_width=True)
                    else:
                        st.write("📕 Capa não disponível.")
                with col2:
                    st.markdown(f"**📖 {row['nome']}**")
                    st.markdown(f"*Autor:* {row['autor']}")
                    if pd.notna(row.get('descricao')) and str(row['descricao']).strip():
                        st.markdown(f"*Descrição:* {row['descricao']}")
                    else:
                        st.markdown("*Descrição não disponível.*")
            st.divider()


        excel_bytes = gerar_excel(df_filtrado[colunas_para_exibir])
        st.download_button(
            label="📥 Exportar para Excel",
            data=excel_bytes,
            file_name="livros_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )