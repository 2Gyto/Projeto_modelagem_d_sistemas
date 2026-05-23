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
| POST | `/simulacoes/teste-integracao` | Front: CEP → Brasil API → SQLite (tarifa) → NASA (HSP mensal) |
| POST | `/simulacoes/hsp` | Somente HSP por CEP (sem tarifa) |

### Tarifas por UF (SQLite)

```bash
python scripts/seed_tarifas_uf.py
```

Gera `src/banco_de_dados/tarifas_por_uf.sqlite` a partir de `tarifas_por_uf.sql`.

## Próximas etapas

1. Motor de cálculo (RF05–RF07, RB01–RB10)
2. Integração completa Brasil API → NASA POWER → Gemini
3. Seed de `tarifas_concessionarias`
4. Conectar o frontend (`front_solarcalc`) à API
