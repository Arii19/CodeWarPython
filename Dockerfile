FROM python:3.11

WORKDIR /app

# Instalar dependências do sistema para compilar libs Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
