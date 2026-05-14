# 🔹 Imagem base
FROM python:3.11-slim

# 🔹 Evita buffer de log
ENV PYTHONUNBUFFERED=1

# 🔹 Diretório dentro do container
WORKDIR /app

# 🔹 Copia requirements primeiro (cache inteligente)
COPY requirements.txt .

# 🔹 Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Copia o resto do projeto
COPY . .

# 🔹 Expõe a porta da API
EXPOSE 8000

# 🔹 Comando para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
