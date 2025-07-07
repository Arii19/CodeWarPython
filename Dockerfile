# Etapa base
FROM python:3.11

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos de onde está a api para dentro do container
COPY . .

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Informa ao Docker que a aplicação usará a porta 8000 (usada por padrão pelo FastAPI)
EXPOSE 8000

# Comando que inicia a aplicação FastAPI com Uvicorn
# --host 0.0.0.0: permite acesso externo ao container
# --port 10000: define a porta onde a app será exposta
# --reload: reinicia automaticamente quando houver alterações no código
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]

