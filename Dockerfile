# Imagem base Python
FROM python:3.12-slim

# Instala pacotes do apt.txt
COPY apt.txt /tmp/apt.txt
RUN apt-get update && \
    xargs apt-get install -y < /tmp/apt.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe porta
EXPOSE 8000

# Comando para rodar o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
