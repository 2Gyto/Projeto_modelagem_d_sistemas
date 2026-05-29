# SolarCalc — Backend API

API REST em **Python + FastAPI**, monólito em camadas (ADR-02), persistência **PostgreSQL** (ADR-06).

## Estrutura

```
app/
├── domain/           # enums e exceções de negócio
├── application/    # casos de uso (auth, simulação)
├── infrastructure/
│   ├── db/         # SQLAlchemy + modelos
│   ├── http/       # rotas FastAPI
│   └── external/   # clientes Brasil API / NASA (Gemini na próxima etapa)
└── main.py
```

## Pré-requisitos

- Python 3.11+
- Docker (para PostgreSQL) ou instância local do Postgres 16

## Subir o banco

Na raiz do repositório:

```bash
docker compose up -d
```

## Instalação e migração

```bash
cd src/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
```

## Executar a API

```bash
uvicorn app.main:app --reload --app-dir .
```

Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Testes unitários

Na pasta `src/backend`:

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes ficam em `tests/` e usam mocks para banco (SQLAlchemy `Session`) e HTTP (`httpx`). Não é necessário PostgreSQL rodando para a suíte padrão.

## Endpoints (prefixo `/api/v1`)

| Método | Caminho | Descrição |
|--------|---------|-----------|
| GET | `/health` | Saúde da API |
| POST | `/auth/register` | Cadastro |
| POST | `/auth/login` | Login (JWT) |
| GET | `/auth/me` | Perfil (Bearer) |
| POST | `/simulacoes` | Criar rascunho de simulação |
| GET | `/simulacoes` | Listar simulações do usuário |
| GET | `/simulacoes/{id}` | Detalhe |
| POST | `/simulacoes/{id}/executar` | **501** — motor de cálculo (próxima etapa) |

## Próximas etapas

1. Motor de cálculo (RF05–RF07, RB01–RB10)
2. Integração completa Brasil API → NASA POWER → Gemini
3. Seed de `tarifas_concessionarias`
4. Conectar o frontend (`front_solarcalc`) à API
