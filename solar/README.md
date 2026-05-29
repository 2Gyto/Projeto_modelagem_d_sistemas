# SolarCalc

Simulador web de viabilidade de sistemas fotovoltaicos. O usuário informa o CEP
e o gasto mensal de energia, deixa nome e e-mail, e recebe um dashboard com a
quantidade de placas solares necessárias, potência do sistema, geração estimada
e economia mensal.

> Versão MVP. Os parâmetros de cálculo (tarifa, HSP, eficiência) são valores
> médios brasileiros. As próximas iterações vão integrar Brasil API (CEP →
> coordenadas), NASA POWER (irradiação real da região) e Gemini (cotação
> dinâmica de equipamentos).

---

## Sumário

- [Stack](#stack)
- [Arquitetura em uma página](#arquitetura-em-uma-página)
- [Fluxo do usuário](#fluxo-do-usuário)
- [Como rodar localmente](#como-rodar-localmente)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Documentação detalhada](#documentação-detalhada)

---

## Stack

| Camada       | Tecnologia                                                          |
| ------------ | ------------------------------------------------------------------- |
| Backend      | Python 3.12 · FastAPI · SQLAlchemy 2 · Pydantic 2 · Alembic         |
| Banco        | PostgreSQL 16 (via Docker Compose)                                  |
| Frontend     | HTML + Bootstrap 5 + JS vanilla servidos pelo próprio FastAPI       |
| Autenticação | JWT (no fluxo autenticado opcional; o fluxo público não exige login) |

---

## Arquitetura em uma página

Monólito FastAPI organizado em três camadas:

```
┌──────────────────────────────────────────────────────────┐
│  Frontend  (static + templates servidos pelo FastAPI)    │
│  index.html  ──POST /api/v1/simulacoes/publica──▶        │
│  dashboard.html  ◀──GET  /api/v1/simulacoes/publica/:id──│
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────────┐
│  Infrastructure / HTTP                                   │
│  routers/ · schemas Pydantic · dependencies (DB, auth)   │
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────────┐
│  Application                                             │
│  SimulacaoPublicaService · CalculadoraSolar · AuthService│
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────────┐
│  Domain                                                  │
│  enums (StatusSimulacao, TipoEntradaConsumo, ...)        │
│  exceptions (DomainError, EntityNotFoundError, ...)      │
└──────────────────┬───────────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────────┐
│  Infrastructure / DB                                     │
│  SQLAlchemy models · session · migrations Alembic        │
│  PostgreSQL                                              │
└──────────────────────────────────────────────────────────┘
```

Mais detalhes em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

---

## Fluxo do usuário

1. Usuário acessa `/`, preenche **CEP** e **gasto médio mensal (R$)** e clica em
   **Simular**.
2. Modal pede **nome** e **e-mail** (captura de lead).
3. Frontend faz `POST /api/v1/simulacoes/publica` com `{nome, email, cep,
   valor_reais}`.
4. Backend:
   - faz upsert do usuário pelo e-mail (sem senha — é lead);
   - cria `simulacao`, `dados_consumo`, `localizacao`;
   - roda a calculadora solar;
   - persiste o `resultado` (nº de placas, potência, geração, economia).
5. Frontend redireciona para `/dashboard?id=<uuid>`.
6. `dashboard.html` chama `GET /api/v1/simulacoes/publica/{id}` e exibe os
   números calculados.

Detalhes do cálculo em [`docs/CALCULO.md`](docs/CALCULO.md).
Contrato de cada endpoint em [`docs/API.md`](docs/API.md).

---

## Como rodar localmente

Pré-requisitos: Docker + Docker Compose, Python 3.12.

```bash
# 1. Subir o Postgres
docker compose up -d

# 2. Criar venv e instalar dependências do backend
cd src/backend
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. (opcional) copiar .env.example -> .env e ajustar se preciso
cp .env.example .env

# 4. Rodar migrations
PYTHONPATH=. .venv/bin/alembic upgrade head

# 5. Subir a API + frontend (mesma porta)
PYTHONPATH=. .venv/bin/uvicorn app.main:app --reload
```

Abra <http://127.0.0.1:8000/>.

> O `docker-compose.yml` mapeia o Postgres em **`localhost:5433`** (não 5432)
> para não conflitar com instalações locais. Se você quiser usar outra porta,
> ajuste tanto o compose quanto `DATABASE_URL` no `.env`.

Mais opções (rodar testes manuais via curl, resetar DB, criar novas migrations)
em [`docs/DESENVOLVIMENTO.md`](docs/DESENVOLVIMENTO.md).

---

## Estrutura de pastas

```
solarcalc/
├── docker-compose.yml             # Postgres 16
├── docs/                          # documentação detalhada
│   ├── ARQUITETURA.md
│   ├── API.md
│   ├── CALCULO.md
│   └── DESENVOLVIMENTO.md
└── src/
    ├── backend/                   # FastAPI + SQLAlchemy + Alembic
    │   ├── alembic/               # migrations
    │   ├── alembic.ini
    │   ├── app/
    │   │   ├── main.py            # bootstrap FastAPI + mount estático
    │   │   ├── config.py          # Settings (env vars)
    │   │   ├── domain/            # enums + exceptions (camada pura)
    │   │   ├── application/       # services + calculadora
    │   │   └── infrastructure/
    │   │       ├── db/            # models + session + base
    │   │       ├── http/          # routers + schemas + dependencies
    │   │       └── external/      # clients (Brasil API, NASA POWER)
    │   ├── requirements.txt
    │   └── .env.example
    └── front_solarcalc/           # frontend estático
        ├── templates/
        │   ├── index.html         # formulário principal
        │   └── dashboard.html     # tela de resultado
        └── static/
            ├── css/style.css
            ├── img/...
            └── js/
                ├── wizard.js      # validação + POST da simulação
                └── dashboard.js   # busca + render do resultado
```

---

## Documentação detalhada

- [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) — camadas, responsabilidades,
  diagrama do banco, decisões de design.
- [`docs/API.md`](docs/API.md) — endpoints, payloads, códigos de erro.
- [`docs/CALCULO.md`](docs/CALCULO.md) — fórmula da calculadora solar passo a
  passo, parâmetros e exemplo numérico.
- [`docs/DESENVOLVIMENTO.md`](docs/DESENVOLVIMENTO.md) — setup, migrations,
  reset de DB, dicas para evoluir.
