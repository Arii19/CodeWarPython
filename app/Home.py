import requests
import pandas as pd
import streamlit as st
from typing import Optional


BASE_URL: str = "https://api-biblioteca-lg6i.onrender.com/livros"
st.set_page_config(page_title="Biblioteca", layout="wide")


# ========== FUNÇÕES AUXILIARES ========== #
def extract() -> pd.DataFrame:
    """
    Extrai os dados dos livros da API REST.
    Retorna:
        pd.DataFrame: DataFrame contendo os livros, vazio se erro.
    """
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        dados = response.json()
        return pd.DataFrame(dados) if dados else pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao acessar a API: {e}")
        return pd.DataFrame()


def aplicar_css() -> None:
    """
    Aplica o CSS customizado carregando o arquivo style.css local.
    """
    try:
        with open("app/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Arquivo style.css não encontrado. Estilos personalizados não aplicados.")


def formulario_adicionar() -> None:
    """
    Exibe formulário para adicionar um novo livro à base via API.
    """
    st.markdown("<h3 style='text-align: center;'>➕ Adicionar Livro</h3>", unsafe_allow_html=True)
    nome: str = st.text_input("Título para adicionar")
    autor: str = st.text_input("Autor para adicionar")
    descricao: str = st.text_area("Descrição para adicionar")
    genero: str = st.text_input("Gênero para adicionar")
    capa_imagem = st.file_uploader("Capa do Livro (jpg, png) - opcional", type=["jpg", "png", "jpeg"])

    # Simula o upload da capa e gera uma URL fictícia para demonstração
    capa_url: Optional[str] = f"https://meusite.com/imagens/{capa_imagem.name}" if capa_imagem else None

    if st.button("Adicionar Livro"):
        if not (nome and autor and descricao and genero):
            st.warning("Preencha todos os campos obrigatórios.")
            return
        df_livros = extract()

        # Verifica se já existe um livro com o mesmo nome e autor (ignora maiúsculas/minúsculas)
        existe_repetido = (
            (df_livros["nome"].str.lower() == nome.lower()) &
            (df_livros["autor"].str.lower() == autor.lower())
        ).any()

        if existe_repetido:
            st.warning("Livro já existe na biblioteca. Não é possível adicionar duplicado.")
            return

        dados = {"nome": nome, "autor": autor, "descricao": descricao, "genero": genero}
        if capa_url:
            dados["capa"] = capa_url

        res = requests.post(BASE_URL, json=dados)
        if res.status_code in (200, 201):
            st.success("Livro adicionado com sucesso!")
            st.rerun()
        else:
            st.error(f"Erro ao adicionar: {res.status_code}")
            st.write(res.text)


def exibir_card_livro(row: pd.Series, idx: int) -> str:
    """
    Gera o HTML para o card do livro, com suporte para descrição expandida.
    Args:
        row (pd.Series): Linha do DataFrame contendo dados do livro.
        idx (int): Índice único para controle do toggle da descrição.
    Returns:
        str: Código HTML do card.
    """
    capa_html = (
        f'<img src="{row["capa"]}" class="livro-imagem"/>'
        if pd.notna(row.get("capa")) and row["capa"].strip() != ""
        else '<div class="livro-imagem" style="background:#444; display:flex; align-items:center; justify-content:center; color:#AAA; width:200px; height:280px; border-radius:12px;">📕 Sem Capa</div>'
    )

    descricao_completa = row.get("descricao", "Descrição não disponível.")
    limite = 150
    resumo = descricao_completa[:limite] + "..." if len(descricao_completa) > limite else descricao_completa
    unique_id = f"toggle_{idx}"

    if len(descricao_completa) > limite:
        return f"""
        <div class="livro-card">
            {capa_html}
            <div class="livro-info">
                <div class="linha-titulo-autor">
                    <h3>📖 {row['nome']}</h3>
                    <p class="autor">{row['autor']}</p>
                </div>
                <p class="descricao">{resumo}</p>
                <input type="checkbox" id="{unique_id}" />
                <label for="{unique_id}"></label>
                <div class="expandido_{unique_id}">{descricao_completa}</div>
            </div>
        </div>
        <style>
            #{unique_id} {{ display: none; }}
            label[for="{unique_id}"] {{
                color: #0E76A8; cursor: pointer; font-weight: bold; margin-top: 0.5rem; display: inline-block;
            }}
            .expandido_{unique_id} {{ display: none; margin-top: 0.5rem; font-size: 14px; color: #CCCCCC; }}
            #{unique_id}:checked ~ .expandido_{unique_id} {{ display: block; }}
            label[for="{unique_id}"]::after {{ content: " (Leia mais)"; }}
            #{unique_id}:checked + label[for="{unique_id}"]::after {{ content: " (Leia menos)"; }}
        </style>
        """
    else:
        return f"""
        <div class="livro-card">
            {capa_html}
            <div class="livro-info">
                <div class="linha-titulo-autor">
                    <h3>📖 {row['nome']}</h3>
                    <p class="autor">{row['autor']}</p>
                </div>
                <p class="descricao">{descricao_completa}</p>
            </div>
        </div>
        """
   
def exibir_livros(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Exibe lista paginada de livros com filtro por busca.
    Args:
        df (pd.DataFrame): DataFrame com os livros.
    Returns:
        Optional[pd.DataFrame]: DataFrame filtrado ou None se vazio.
    """
    st.divider()
    busca = st.text_input("🔎 Buscar livros (por título, autor ou gênero)", key="busca_livros").strip()

    df_filtrado = df.copy()

    if busca:
        busca_lower = busca.lower()
        df_filtrado = df_filtrado[
            df_filtrado["nome"].str.lower().str.contains(busca_lower)
            | df_filtrado["autor"].str.lower().str.contains(busca_lower)
            | df_filtrado["genero"].str.lower().str.contains(busca_lower)
        ]

    if df_filtrado.empty:
        st.warning("Nenhum livro encontrado.")
        return None

    filtros_padrao = not busca

    if filtros_padrao:
        st.markdown("<h3 style='text-align: center;'>📙➕ Quem sabe essa pode ser sua próxima leitura</h3>", unsafe_allow_html=True)
        df_para_exibir = df_filtrado[df_filtrado["capa"].notna() & (df_filtrado["capa"].str.strip() != "")]
    else:
        st.markdown("### 🖼️ Saiba mais sobre os livros")
        df_para_exibir = df_filtrado

    livros_por_pagina = 4
    total_paginas = (len(df_para_exibir) - 1) // livros_por_pagina + 1
    pagina_atual = st.number_input("📄 Página", min_value=1, max_value=total_paginas, value=1, step=1)

    inicio = (pagina_atual - 1) * livros_por_pagina
    fim = inicio + livros_por_pagina
    df_pagina = df_para_exibir.iloc[inicio:fim]

    for i in range(0, len(df_pagina), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(df_pagina):
                break
            row = df_pagina.iloc[idx]
            col.markdown(exibir_card_livro(row, idx), unsafe_allow_html=True)

    return df_filtrado


def painel_edicao(livro: pd.Series) -> None:
    """
    Exibe painel para editar ou excluir livro selecionado.

    Args:
        livro (pd.Series): Linha com os dados do livro a ser editado.
    """
    st.markdown("### ✏️ Atualizar ou Excluir Livro")
    st.markdown(f"**Selecionado:** 📖 {livro['nome']} - {livro['autor']}")

    # Inicializa session_state para manter valores de edição sincronizados
    if (
        "novo_nome" not in st.session_state
        or st.session_state.get("id_livro_editando") != livro["id"]
    ):
        st.session_state.novo_nome = livro.get("nome", "")
        st.session_state.novo_autor = livro.get("autor", "")
        st.session_state.nova_descricao = livro.get("descricao", "")
        st.session_state.novo_genero = livro.get("genero", "")
        st.session_state.nova_capa = livro.get("capa", "")
        st.session_state.id_livro_editando = livro["id"]
        if "confirm_excluir" not in st.session_state:
            st.session_state.confirm_excluir = False

    novo_nome = st.text_input("Novo nome", value=st.session_state.novo_nome, key="novo_nome")
    novo_autor = st.text_input("Novo autor", value=st.session_state.novo_autor, key="novo_autor")
    nova_descricao = st.text_area("Nova descrição", value=st.session_state.nova_descricao, key="nova_descricao")
    novo_genero = st.text_input("Novo gênero", value=st.session_state.novo_genero, key="novo_genero")
    nova_capa = st.text_input("Nova URL da capa", value=st.session_state.nova_capa, key="nova_capa")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Atualizar livro"):
            dados = {
                "nome": novo_nome,
                "autor": novo_autor,
                "descricao": nova_descricao,
                "genero": novo_genero,
                "capa": nova_capa,
            }
            res = requests.put(f"{BASE_URL}/{livro['id']}", json=dados)
            if res.status_code == 200:
                st.success("✅ Atualizado com sucesso!")
                st.rerun()
            else:
                st.error(f"Erro ao atualizar: {res.status_code}")
                st.write(res.text)

    with col2:
        confirm = st.checkbox("☑️ Confirmo que desejo excluir este livro", key="confirm_excluir")
        if st.button("🗑️ Excluir livro"):
            if confirm:
                res = requests.delete(f"{BASE_URL}/{livro['id']}")
                if res.status_code == 200:
                    st.success("❌ Livro excluído!")
                    st.rerun()
                else:
                    st.error(f"Erro ao excluir: {res.status_code}")
                    st.write(res.text)
            else:
                st.warning("Marque a confirmação para excluir.")


def main() -> None:
    """
    Função principal que executa o app Streamlit.
    """
    aplicar_css()

    st.markdown("<h1>📚 Bem-vindo ao Cantinho da Leitura</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Explore suas leituras, exporte informações e acompanhe seu progresso</h4>", unsafe_allow_html=True)
    st.divider()

    formulario_adicionar()

    df = extract()
    if df.empty:
        st.warning("Nenhum dado encontrado.")
        return
    
    df_filtrado = exibir_livros(df)

    if df_filtrado is not None and not df_filtrado.empty:
        opcoes = df_filtrado.apply(lambda row: f"{row['nome']} - {row['autor']}", axis=1).tolist()
        escolha = st.selectbox("Selecione o livro para editar/excluir", opcoes)
        indice = opcoes.index(escolha)
        painel_edicao(df_filtrado.iloc[indice])


if __name__ == "__main__":
    main()
