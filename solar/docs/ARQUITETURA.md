# Arquitetura

O SolarCalc é um **monólito FastAPI organizado em três camadas** (domain →
application → infrastructure). O frontend é estático e servido pela própria
API.

---

## Visão geral em camadas

```
        ┌───────────────────────────────────────────────────┐
        │  Frontend (HTML + Bootstrap + JS vanilla)         │
        │  templates/index.html, templates/dashboard.html   │
        │  static/js/wizard.js, static/js/dashboard.js      │
        └────────────────────┬──────────────────────────────┘
                             │  fetch JSON  /api/v1/...
                             ▼
        ┌───────────────────────────────────────────────────┐
        │  infrastructure/http   (adapters HTTP)            │
        │  routers/, schemas Pydantic, dependencies         │
        └────────────────────┬──────────────────────────────┘
                             │
                             ▼
        ┌───────────────────────────────────────────────────┐
        │  application           (regras + orquestração)    │
        │  *_service.py · calculadora_solar.py              │
        └────────────────────┬──────────────────────────────┘
                             │
                             ▼
        ┌───────────────────────────────────────────────────┐
        │  domain                (modelo puro)              │
        │  enums.py · exceptions.py                         │
        └────────────────────┬──────────────────────────────┘
                             │
                             ▼
        ┌───────────────────────────────────────────────────┐
        │  infrastructure/db     (persistência)             │
        │  models.py (SQLAlchemy) · session.py · base.py    │
        └────────────────────┬──────────────────────────────┘
                             │
                             ▼
                       PostgreSQL 16
```

A regra de dependência é unidirecional: **camadas de cima conhecem as de
baixo, nunca o contrário**. A camada `domain` não importa nada de fora dela.
A camada `application` importa `domain` e tipos de SQLAlchemy (que são
infraestrutura) — esse acoplamento é proposital para manter o monólito
simples; trocar SQLAlchemy exigiria reescrever os services.

---

## Camada `domain`

Arquivos: [`app/domain/enums.py`](../src/backend/app/domain/enums.py),
[`app/domain/exceptions.py`](../src/backend/app/domain/exceptions.py).

Contém apenas tipos puros:

- **Enums** que valem para o modelo todo:
  `TipoEntradaConsumo`, `OrientacaoTelhado`, `TipoConexao`,
  `StatusSimulacao`.
- **Exceções de domínio**: `DomainError`, `EntityNotFoundError`,
  `EmailAlreadyRegisteredError`, `InvalidCredentialsError`,
  `ExternalApiError`.

Por que isolar? Porque as exceções aqui são traduzidas em códigos HTTP
específicos no `main.py` (`DomainError` → 422, `ExternalApiError` → 503) e
queremos poder lançá-las de qualquer camada acima sem dependência circular.

---

## Camada `application`

Arquivos:
- [`app/application/simulacao_publica_service.py`](../src/backend/app/application/simulacao_publica_service.py)
  — fluxo público sem login.
- [`app/application/simulacao_service.py`](../src/backend/app/application/simulacao_service.py)
  — fluxo autenticado (rascunhos, listagem por usuário).
- [`app/application/calculadora_solar.py`](../src/backend/app/application/calculadora_solar.py)
  — função pura que calcula nº de placas a partir do gasto.
- [`app/application/auth_service.py`](../src/backend/app/application/auth_service.py)
  — registro, login, JWT.
- [`app/application/security.py`](../src/backend/app/application/security.py)
  — hash de senha (bcrypt) + emissão/decodificação de JWT.

Cada service recebe uma `Session` SQLAlchemy no construtor e expõe métodos de
caso de uso (não CRUD). Por exemplo, `SimulacaoPublicaService.executar(dados)`
orquestra: upsert do lead → persiste simulação → roda calculadora → persiste
resultado → retorna DTO.

A **calculadora não tem dependência de banco nem de framework** — é uma
função pura, fácil de testar.

---

## Camada `infrastructure`

### `infrastructure/http`

- [`schemas.py`](../src/backend/app/infrastructure/http/schemas.py) — DTOs
  Pydantic (request/response). Inclui `SimulacaoPublicaCreate`,
  `SimulacaoPublicaResponse`, `UsuarioCreate`, `LoginRequest`, etc.
- [`dependencies.py`](../src/backend/app/infrastructure/http/dependencies.py)
  — injeção: `get_db`, `get_auth_service`, `get_current_user` (lê JWT do
  header).
- `routers/`:
  - [`health.py`](../src/backend/app/infrastructure/http/routers/health.py)
    — `GET /health`.
  - [`auth.py`](../src/backend/app/infrastructure/http/routers/auth.py)
    — `POST /auth/register`, `POST /auth/login`, `GET /auth/me`.
  - [`simulacoes.py`](../src/backend/app/infrastructure/http/routers/simulacoes.py)
    — fluxo autenticado (CRUD parcial + placeholder de `/executar`).
  - [`simulacao_publica.py`](../src/backend/app/infrastructure/http/routers/simulacao_publica.py)
    — **fluxo principal do MVP**: `POST /simulacoes/publica` e
    `GET /simulacoes/publica/{id}`, sem autenticação.

Todos sob o prefixo `/api/v1` (vem de `Settings.api_prefix`).

### `infrastructure/db`

- [`base.py`](../src/backend/app/infrastructure/db/base.py) — `DeclarativeBase`
  do SQLAlchemy 2.
- [`session.py`](../src/backend/app/infrastructure/db/session.py) — engine +
  `SessionLocal` + função `get_db` (generator usado como dependência).
- [`models.py`](../src/backend/app/infrastructure/db/models.py) — ORM.

### `infrastructure/external`

Clients HTTP assíncronos para APIs de terceiros. **Ainda não conectados ao
fluxo principal**, ficam prontos para a próxima iteração:

- [`brasil_api.py`](../src/backend/app/infrastructure/external/brasil_api.py)
  — `buscar_cep(cep)` em `brasilapi.com.br`.
- [`nasa_power.py`](../src/backend/app/infrastructure/external/nasa_power.py)
  — `buscar_irradiacao_mensal(lat, lon)` em `power.larc.nasa.gov`.
- [`base_client.py`](../src/backend/app/infrastructure/external/base_client.py)
  — wrapper com timeout + tradução de erros para `ExternalApiError`.

---

## Modelo de dados

```
usuarios ─────────────┐
   id (uuid)          │ 1
   nome               │
   email (uniq)       │
   senha_hash (NULL)  │  NULL ⇒ usuário capturado pelo fluxo público (lead)
   criado_em          │
                      │ N
                      ▼
                  simulacoes
                     id (uuid)
                     usuario_id ─┐
                     status      │  enum StatusSimulacao
                     realizada_em│
                                 │
       ┌─────────────────────────┼─────────────────────────┐
       │ 1                       │ 1                       │ 1
       ▼                         ▼                         ▼
  dados_consumo            localizacoes             dados_telhado
     simulacao_id (uniq)     simulacao_id (uniq)     simulacao_id (uniq)
     consumo_kwh             cep                     area_m2 (NULL)
     valor_reais             cidade                  orientacao (NULL)
     tipo_entrada            latitude                tipo_conexao (NULL)
                             longitude
                                 │
                                 │ 1
                                 ▼
                            resultados
                               simulacao_id (uniq)
                               geracao_kwh
                               economia_mensal
                               payback_anos
                               payback_meses
                               custo_total
                               quantidade_paineis      ← novo, MVP
                               potencia_sistema_kwp    ← novo, MVP
                                 │
                                 │ N
                                 ▼
                          projecoes_anuais
                             resultado_id
                             ano, custo_concessionaria,
                             custo_fotovoltaico, saldo

  tarifas_concessionarias  (tabela de referência, isolada)
```

### Decisões de schema relevantes

- **`usuarios.senha_hash` é NULL**: leads capturados pelo fluxo público não
  têm senha. Se um dia quiserem login, geramos uma senha via "esqueci minha
  senha".
- **`dados_telhado.area_m2 / orientacao / tipo_conexao` são NULL**: o fluxo
  público MVP não pergunta esses campos. O fluxo autenticado continua exigindo
  no Pydantic (`SimulacaoCreate` em `schemas.py`).
- **`resultados.quantidade_paineis`** e **`resultados.potencia_sistema_kwp`**
  foram adicionados na migration `002_fluxo_publico.py` para guardar o
  resultado do MVP.
- **UUIDs como PK** em todas as tabelas de domínio — facilita exposição em URL
  sem leak de ordem.

### Migrations

`alembic/versions/`:

- `001_schema_inicial.py` — schema completo inicial.
- `002_fluxo_publico.py` — torna senha/telhado opcionais e adiciona campos do
  MVP em `resultados`.

---

## Frontend

Frontend é puramente estático (HTML + Bootstrap + JS vanilla) servido pela
própria FastAPI:

- `app.mount("/static", StaticFiles(...))` em `main.py`.
- Rotas `/` e `/dashboard` retornam `FileResponse` dos templates.

Vantagem dessa escolha: zero CORS, zero build step, deploy de uma coisa só.
Trocaria por SPA + build (Vite/Next) quando o frontend ficasse complexo o
suficiente para justificar.

### Páginas

- `templates/index.html` — formulário "1) tipo de instalação, 2) CEP,
  3) gasto" → modal "nome + email" → submit.
  Script: `static/js/wizard.js`.
- `templates/dashboard.html` — lê `?id=...`, busca a simulação, mostra nº de
  placas em destaque e métricas de apoio (consumo, potência, geração,
  economia).
  Script: `static/js/dashboard.js`.

---

## Fluxo de uma requisição (caminho feliz)

```
POST /api/v1/simulacoes/publica  {nome,email,cep,valor_reais}
  │
  │   FastAPI: roteia para simulacao_publica.criar_simulacao_publica
  │
  ▼
SimulacaoPublicaService.executar(dados)
  │   ├── _upsert_lead(nome, email)                   ── tabela usuarios
  │   ├── new Simulacao(status=CALCULANDO)            ── tabela simulacoes
  │   ├── new DadosConsumo(...)                       ── tabela dados_consumo
  │   ├── new Localizacao(cep=...)                    ── tabela localizacoes
  │   ├── calcular_paineis_por_gasto(valor_reais)     ── função pura
  │   ├── new Resultado(...)                          ── tabela resultados
  │   ├── sim.status = CONCLUIDA + commit
  │   └── return SimulacaoPublicaResponse(...)
  ▼
HTTP 201 + JSON com simulacao_id, quantidade_paineis, etc.
```

---

## Decisões de design (mini-ADRs)

1. **Monólito em camadas, não DDD completo nem microsserviços.**
   Projeto pequeno; complexidade extra não compensaria. Limites entre camadas
   funcionam como linhas-guia, não barreiras.

2. **Fluxo público sem autenticação.**
   Captura de lead conta mais do que conta protegida nessa fase. Quem quiser
   acompanhar histórico depois usa o fluxo autenticado (rotas `/auth/*` +
   `/simulacoes`).

3. **Calculadora como função pura.**
   `calcular_paineis_por_gasto(valor_reais)` não conhece banco nem framework
   — fácil de testar e de evoluir (substituir constantes por chamadas reais a
   Brasil API / NASA / Gemini).

4. **`Decimal` em vez de `float` no domínio financeiro.**
   Evita imprecisão de ponto flutuante quando o output é dinheiro.

5. **Frontend servido pela mesma origem da API.**
   Elimina CORS. Custo: backend e frontend só conseguem deployar juntos.
