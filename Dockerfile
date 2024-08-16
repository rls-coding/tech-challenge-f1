# Utilize uma imagem base com Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Exponha a porta que a aplicação FastAPI irá utilizar
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI (ajuste se necessário)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]