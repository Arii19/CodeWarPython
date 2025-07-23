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
            height: 280px;
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

# ... seu código e CSS aqui ...

st.set_page_config(page_title="Biblioteca", layout="wide")

# Cabeçalho
st.markdown("<h1>📚 Bem-vindo ao Cantinho da Leitura</h1>", unsafe_allow_html=True)
st.markdown("<h4>Explore suas leituras, exporte informações das suas leituras e acompanhe o seu progresso</h4>", unsafe_allow_html=True)
st.divider()

# Formulário para adicionar livros (opcional - você já tem, pode deixar ou tirar)
nome = st.text_input("Título para adicionar")
autor = st.text_input("Autor para adicionar")
descricao = st.text_area("Descrição para adicionar")
genero = st.text_input("Gênero para adicionar")
capa_imagem = st.file_uploader("Capa do Livro (jpg, png) - opcional", type=["jpg", "png", "jpeg"])

capa_url = None
if capa_imagem:
    capa_url = f"https://meusite.com/imagens/{capa_imagem.name}"  # simulação

if st.button("Adicionar Livro", key="botao_adicionar_livro"):
    if not (nome and autor and descricao and genero):
        st.warning("Preencha todos os campos obrigatórios para adicionar um livro.")
    else:
        dados = {"nome": nome, "autor": autor, "descricao": descricao, "genero": genero}
        if capa_url:
            dados["capa"] = capa_url

        res = requests.post(BASE_URL, json=dados)
        if res.status_code in [200, 201]:
            st.success("Livro adicionado com sucesso!")
        else:
            st.error(f"Erro ao adicionar livro: {res.status_code}")
            st.write(res.text)
        st.divider()

# *** BUSCA FICA AQUI, DEPOIS DO FORMULÁRIO ***

busca = st.text_input("🔎 Buscar livros (por título, autor ou gênero)")

# Extração dos dados da API
df = extract()

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a API.")
else:
    df_filtrado = df.copy()
    if busca.strip():
        busca_lower = busca.lower()
        df_filtrado = df_filtrado[
            df_filtrado['nome'].str.lower().str.contains(busca_lower) |
            df_filtrado['autor'].str.lower().str.contains(busca_lower) |
            df_filtrado['genero'].str.lower().str.contains(busca_lower)
        ]

    if df_filtrado.empty:
        st.warning("Nenhum livro encontrado para a busca realizada.")
    else:
        filtros_padrao = not busca.strip()

        st.divider()
        if filtros_padrao:
            st.markdown("<h2 style='text-align: center;'>📙➕Quem sabe essa pode ser sua próxima leitura</h2>", unsafe_allow_html=True)
            df_para_exibir = df_filtrado[df_filtrado['capa'].notna() & (df_filtrado['capa'].str.strip() != '')]
        else:
            st.markdown("### 🖼️ Saiba mais sobre os livros")
            df_para_exibir = df_filtrado

        # Paginação e exibição
        livros_por_pagina = 4
        total_livros = len(df_para_exibir)
        total_paginas = (total_livros - 1) // livros_por_pagina + 1

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

                capa_html = (
                    f'<img src="{row["capa"]}" class="livro-imagem"/>'
                    if pd.notna(row.get('capa')) and row['capa'].strip() != ''
                    else '<div class="livro-imagem" style="background:#444; display:flex; align-items:center; justify-content:center; color:#AAA; width:200px; height:280px; border-radius:12px;">📕 Sem Capa</div>'
                )

                descricao_completa = row['descricao'] if pd.notna(row.get('descricao')) else "Descrição não disponível."
                limite = 150
                resumo = descricao_completa[:limite] + "..." if len(descricao_completa) > limite else descricao_completa
                unique_id = f"toggle_{idx}"

                if len(descricao_completa) > limite:
                    card_html = f"""
                    <style>
                      #{unique_id} {{ display: none; }}
                      label[for="{unique_id}"] {{
                        color: #0E76A8;
                        cursor: pointer;
                        font-weight: bold;
                        margin-top: 0.5rem;
                        display: inline-block;
                      }}
                      .expandido_{unique_id} {{ display: none; margin-top: 0.5rem; font-size: 14px; color: #CCCCCC; }}
                      #{unique_id}:checked ~ .expandido_{unique_id} {{ display: block; }}
                      #{unique_id}:checked + label[for="{unique_id}"]::after {{ content: " (Leia menos)"; }}
                      label[for="{unique_id}"]::after {{ content: " (Leia mais)"; }}
                    </style>

                    <div class="livro-card">
                      {capa_html}
                      <div class="livro-info">
                        <div class="linha-titulo-autor">
                          <h3>📖 {row['nome']}</h3>
                          <p class="autor">{row['autor']}</p>
                        </div>
                        <p class="descricao">{resumo}</p>
                        <input type="checkbox" id="{unique_id}"/>
                        <label for="{unique_id}"></label>
                        <div class="expandido_{unique_id}">{descricao_completa}</div>
                      </div>
                    </div>
                    """
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
                col.markdown(card_html, unsafe_allow_html=True)

        st.divider()

        # --- Atualizar ou Deletar livro ---

        st.markdown("### ✏️ Atualizar ou Excluir Livro")

        # Usa o primeiro livro do resultado da busca para atualizar/deletar
        livro = df_filtrado.iloc[0]

        st.markdown(f"**Livro selecionado:** 📖 {livro['nome']} - Autor: {livro['autor']}")

        novo_nome = st.text_input("Novo nome", value=livro.get("nome", ""))
        novo_autor = st.text_input("Novo autor", value=livro.get("autor", ""))
        nova_descricao = st.text_area("Nova descrição", value=livro.get("descricao", ""))
        novo_genero = st.text_input("Novo gênero", value=livro.get("genero", ""))
        nova_capa = st.text_input("Nova URL da capa", value=livro.get("capa", ""))

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Atualizar livro"):
                dados_atualizados = {
                    "nome": novo_nome,
                    "autor": novo_autor,
                    "descricao": nova_descricao,
                    "genero": novo_genero,
                    "capa": nova_capa
                }
                r = requests.put(f"{BASE_URL}/{livro['id']}", json=dados_atualizados)
                if r.status_code == 200:
                    st.success("✅ Livro atualizado com sucesso!")
                else:
                    st.error(f"Erro ao atualizar: {r.status_code}")
                    st.write(r.text)

        with col2:
            confirm = st.checkbox("☑️ Confirmo que desejo excluir este livro")
            if st.button("🗑️ Excluir livro"):
                if confirm:
                    r = requests.delete(f"{BASE_URL}/{livro['id']}")
                    if r.status_code == 200:
                        st.success("❌ Livro excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao excluir: {r.status_code}")
                        st.write(r.text)
                else:
                    st.warning("☝️ Marque a confirmação para excluir antes de clicar no botão.")