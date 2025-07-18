from turtle import left
import requests
import pandas as pd
import streamlit as st
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

st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4 {
            text-align: center;
            color: #D2E0E2;
                .stDownloadButton>button {
            background-color: #0E76A8;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }

        .stDownloadButton>button:hover {
            background-color: #075E8D;
            color: white;
        }
        }
        .livro-card {
            background-color: #232326;
            padding: 1rem;
            border-radius: 12px;
            max-width: 700px;
            display: flex;
            gap: 1rem;
            align-items: flex-start;
            color: #CCCCCC;
            margin-bottom: 1.5rem;
        }

        .livro-imagem {
            width: 200px;
            height: auto;
            border-radius: 12px;
            flex-shrink: 0;
            object-fit: cover;
        }

        .livro-info {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .linha-titulo-autor {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            flex-wrap: nowrap;
        }

        .linha-titulo-autor h3 {
            margin: 0;
            color: #D2E0E2;
            font-weight: 700;
        }

        .linha-titulo-autor p.autor {
            margin: 0;
            color: #A0C4FF;
            font-weight: 600;
            white-space: nowrap;
        }

        .descricao {
            margin-top: 0.5rem;
            font-size: 14px;
            line-height: 1.4;
            color: #CCCCCC;
        }
            
        .button {
            background-color: #0E76A8;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }

        .stButton > button {
            background-color: #0E76A8 !important;
            color: white !important;
            border: 2px solid #0E76A8 !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            padding: 0.5em 1em !important;
            transition: all 0.2s ease-in-out !important;
            outline: none !important;
            box-shadow: 0 0 6px #0e37a8 !important;
        }

        .stButton > button:hover {
            background-color: #0e37a8 !important;
            border: 2px solid #0e37a8 !important;
            color: white !important;
        }

        .stButton > button:active {
            background-color: #0e37a8 !important;
            color: white !important;
            border: 2px solid #0e37a8 !important;
            outline: none !important;
            box-shadow: none !important;
        }

        input[type=number] {
            border: 1px solid #0E76A8 !important;
            border-radius: 8px !important;
            padding: 0.3em 0.6em !important;
            box-shadow: none !important;
            outline: none !important;
            color: white;
            background-color: #232326;
        }

        input[type=number]:hover {
            border-color: #0E76A8 !important;
            box-shadow: 0 0 5px #0E76A8 !important;
            outline: none !important;
        }

        input[type=number]:focus {
            border-color: #075E8D !important;
            box-shadow: 0 0 5px #075E8D !important;
            outline: none !important;
        }

        input[type=number]::-webkit-inner-spin-button {
            background-color: #232326 !important;
            border: none !important;
            height: auto !important;
            width: 18px !important;
            color: white !important;
        }

        input[type=number]::-moz-inner-spin-button {
            background-color: #232326 !important;
            border: none !important;
            height: auto !important;
            width: 18px !important;
            color: white !important;
        }

        input[type=number]::-webkit-inner-spin-button:hover {
            background-color: #0E76A8 !important;
        }

        input[type=number]::-webkit-inner-spin-button:focus {
            background-color: #075E8D !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Seu layout e inputs para cadastro ---

st.markdown("<h1>📚 Bem-vindo ao Cantinho da Leitura</h1>", unsafe_allow_html=True)
st.markdown("<h4>Explore suas leituras, exporte informações das suas leituras e acompanhe o seu progresso</h4>", unsafe_allow_html=True)
st.divider()

st.set_page_config(page_title="Biblioteca", layout="wide")

st.markdown("<h2 style='text-align: center;'>📚 Insira a sua nova Leitura</h2>", unsafe_allow_html=True)

nome = st.text_input("Título")
autor = st.text_input("Autor")
descricao = st.text_area("Descrição")
genero = st.text_input("Gênero")

capa_imagem = st.file_uploader("Capa do Livro (jpg, png) - opcional", type=["jpg", "png", "jpeg"])

capa_url = None
if capa_imagem:
    # Você pode criar uma lógica para upload da imagem
    capa_url = f"https://meusite.com/imagens/{capa_imagem.name}"

if st.button("Adicionar Livro", key=f"botao_adicionar_livro"):
    if not (nome and autor and descricao and genero):
        st.warning("Preencha todos os campos obrigatórios.")
    else:
        dados = {
            "nome": nome,
            "autor": autor,
            "descricao": descricao,
            "genero": genero,
        }
        if capa_url:
            dados["capa"] = capa_url

        res = requests.post(BASE_URL, json=dados)
        if res.status_code in [200, 201]:
            st.success("Livro adicionado com sucesso!")
        else:
            st.error(f"Erro: {res.status_code}")
            st.write(res.text)
        st.divider()

# --- Extração dos dados ---
df = extract()

def gerar_excel(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_to_export.to_excel(writer, sheet_name="Livros", index=False)
    output.seek(0)
    return output

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a API.")
else:
    genero_opcoes = ['Todos'] + sorted(df['genero'].unique())
    genero = st.sidebar.selectbox("Filtrar por Gênero:", genero_opcoes)

    autor_opcoes = ['Todos'] + sorted(df['autor'].unique())
    autor = st.sidebar.selectbox("Filtrar por Autor:", autor_opcoes)

    titulo = st.sidebar.text_input("Buscar por Título do Livro:")

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
        filtros_padrao = genero == "Todos" and autor == "Todos" and titulo.strip() == ""

        st.divider()
        if filtros_padrao:
            st.markdown("<h2 style='text-align: center;'>📙➕Quem sabe essa pode ser sua próxima leitura</h2>", unsafe_allow_html=True)
            df_para_exibir = df_filtrado[df_filtrado['capa'].notna() & (df_filtrado['capa'].str.strip() != '')]
        else:
            st.markdown("### 🖼️ Saiba mais sobre os livros")
            df_para_exibir = df_filtrado

        livros_por_pagina = 10
        total_livros = len(df_para_exibir)
        total_paginas = (total_livros - 1) // livros_por_pagina + 1

        pagina_atual = st.number_input(
            label="📄 Página",
            min_value=1,
            max_value=total_paginas,
            value=1,
            step=1
        )

        inicio = (pagina_atual - 1) * livros_por_pagina
        fim = inicio + livros_por_pagina
        df_pagina = df_para_exibir.iloc[inicio:fim]

        # --- Exibição dos cards de livros paginados (2 por linha) ---
    for i in range(0, len(df_pagina), 4):
        cols = st.columns([2, 2])  # duas colunas na mesma linha

        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(df_pagina):
                break
            row = df_pagina.iloc[idx]

            with col:
                capa_html = (
                    f'<img src="{row["capa"]}" class="livro-imagem"/>'
                    if pd.notna(row.get('capa')) and row['capa'].strip() != ''
                    else '<div class="livro-imagem" style="background:#444; display:flex; align-items:center; justify-content:center; color:#AAA; width:200px; height:280px; border-radius:12px;">📕 Sem Capa</div>'
                )

                descricao_completa = (
                    row['descricao']
                    if pd.notna(row.get('descricao')) and str(row['descricao']).strip()
                    else "Descrição não disponível."
                )

                limite = 150  # limite de caracteres para o resumo

                if len(descricao_completa) > limite:
                    resumo = descricao_completa[:limite] + "..."
                    unique_id = f"toggle_{idx}"

                    card_html = f"""
                    <style>
                      #{unique_id} {{
                        display: none;
                      }}

                      label[for="{unique_id}"] {{
                        color: #0E76A8;
                        cursor: pointer;
                        font-weight: bold;
                        margin-top: 0.5rem;
                        display: inline-block;
                      }}

                      .expandido_{unique_id} {{
                        display: none;
                        margin-top: 0.5rem;
                        font-size: 14px;
                        color: #CCCCCC;
                      }}

                      #{unique_id}:checked ~ .expandido_{unique_id} {{
                        display: block;
                      }}

                      #{unique_id}:checked + label[for="{unique_id}"]::after {{
                        content: " (Leia menos)";
                      }}

                      label[for="{unique_id}"]::after {{
                        content: " (Leia mais)";
                      }}
                    </style>

                    <div class="livro-card">
                      {capa_html}
                      <div class="livro-info">
                        <div class="linha-titulo-autor">
                          <h3>📖 {row['nome'], left}</h3>
                          <p class="autor">{row['autor'], left}</p>
                        </div>
                        <p class="descricao">{resumo}</p>
                        <input type="checkbox" id="{unique_id}"/>
                        <label for="{unique_id}"></label>
                        <div class="expandido_{unique_id}">{descricao_completa}</div>
                      </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    card_html = f"""
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
                    st.markdown(card_html, unsafe_allow_html=True)
        st.divider()

        st.markdown("### 📖 Tabelas de livros")
        colunas_para_exibir = ['nome', 'autor', 'genero']

        linhas = len(df_filtrado)
        altura_por_linha = 35
        altura_minima = 100
        altura_maxima = 600
        altura_tabela = max(altura_minima, min(linhas * altura_por_linha, altura_maxima))

        st.dataframe(
            df_filtrado[colunas_para_exibir],
            use_container_width=True,
            height=altura_tabela
        )