FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql+psycopg://solarcalc:solarcalc@postgres:5432/solarcalc

# Porta padrão do Uvicorn
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
