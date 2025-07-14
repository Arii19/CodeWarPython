import requests
import pandas as pd
import streamlit as st

BASE_URL = "https://api-biblioteca-lg6i.onrender.com/livros"

def buscar_livros_por_autor(autor):
    try:
        response = requests.get(f"{BASE_URL}/autor/{autor}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar livros: {e}")
        return []