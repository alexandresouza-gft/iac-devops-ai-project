# Dockerfile
FROM python:3.12-slim

# Evita prompts interativos e acelera instalações
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependências do sistema (opcional, ajuste conforme seu requirements)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas requirements primeiro para aproveitar cache
COPY requirements*.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o código
COPY main.py /app/
COPY .env /app/.env


# Streamlit roda na 8501 por padrão
EXPOSE 8501

# Comando padrão: escuta em 0.0.0.0 e porta configurável via env
# Você pode trocar a porta via variável de ambiente SERVER_PORT
ENV SERVER_PORT=8501
CMD ["sh", "-c", "streamlit run main.py --server.address=0.0.0.0 --server.port=${SERVER_PORT}"]
