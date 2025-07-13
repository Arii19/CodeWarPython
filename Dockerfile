# Etapa base
FROM python:3.11

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos da API para dentro do container
COPY . .

# Instala dependências do sistema necessárias para compilação de pacotes Python
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && apt-get clean

# Atualiza pip e ferramentas de build
RUN pip install --upgrade pip setuptools wheel

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Informa ao Docker que a aplicação usará a porta 8000
EXPOSE 8000

# Comando que inicia a aplicação FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
