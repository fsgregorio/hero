FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /main

# Copia os arquivos do projeto para o contêiner
COPY . /main

# Instala dependências do projeto
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
