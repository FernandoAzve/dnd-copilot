# Imagem base oficial do Python 3.11 Slim
FROM python:3.11-slim

# Metadados do projeto
LABEL maintainer="Fernando Azevedo"
LABEL description="D&D Copilot - Assistente e Mentor de Regras D&D 5e/2024"

# Evitar criação de arquivos .pyc e garantir output imediato no console
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Diretório de trabalho na aplicação
WORKDIR /app

# Instalar dependências de sistema para compilação e suporte a PDFs/Imagens
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas os requisitos primeiro para otimizar cache de camadas do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo o código-fonte da aplicação
COPY . .

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Healthcheck para monitorar integridade do container
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para iniciar o D&D Copilot
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
