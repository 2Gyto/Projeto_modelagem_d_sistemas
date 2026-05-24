# SolarCalc — Backend API

API REST em **Python + FastAPI**, monólito em camadas (ADR-02), persistência **PostgreSQL** (ADR-06), tarifas por UF em **SQLite**.

## Pipeline de simulação (`POST /simulacoes/completa`)

1. **Brasil API** — `GET /cep/v2/{cep}` → latitude, longitude, UF  
2. **SQLite** — tarifa e taxas de disponibilidade por UF  
3. **NASA POWER** — irradiação mensal → **HSP** médio (h/dia)  
4. **Motor de cálculo** — geração, investimento, payback, projeção 25 anos  

## Estrutura

```
app/
├── application/     # auth, simulação, cálculo, executor
├── domain/
├── infrastructure/
│   ├── db/          # PostgreSQL + tarifa_sqlite.py
│   └── external/    # Brasil API, NASA POWER
data/
  tarifas_uf.db      # seed automático no startup se ausente
scripts/
  seed_tarifas_uf.py
```

## Subir o banco

Na raiz do repositório:

```bash
docker compose up -d
```

## Instalação

```bash
cd src/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/seed_tarifas_uf.py
alembic upgrade head
```

## Executar

```bash
uvicorn app.main:app --reload --app-dir .
```

- API: http://127.0.0.1:8000/docs  
- Front (estático): http://127.0.0.1:8000/app/templates/index.html  

## Endpoints principais

| Método | Caminho | Descrição |
|--------|---------|-----------|
| POST | `/auth/register` | Cadastro |
| POST | `/auth/login` | JWT |
| POST | `/simulacoes/completa` | Cria + executa pipeline |
| POST | `/simulacoes/{id}/executar` | Executa rascunho existente |
| GET | `/simulacoes/{id}` | Resultado com projeções 25 anos |
