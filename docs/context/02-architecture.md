## Architecture Handoff — SolarCalc (inicial)

### Component map

| Componente | Responsabilidade | Tech |
|------------|------------------|------|
| API REST | Autenticação, CRUD de simulações, orquestração | FastAPI (Python) |
| Motor de cálculo | Payback, geração, projeção 25 anos | Python (application) — *pendente* |
| Integrações externas | CEP, HSP, preços painéis | httpx async, timeout 10s |
| Persistência | Usuários, simulações, tarifas | PostgreSQL 16 + SQLAlchemy |
| Frontend | Wizard + dashboard | HTML/JS estático (existente) |

### API contracts (v1, prefixo `/api/v1`)

- `POST /auth/register` — `{ nome, email, senha }` → `Usuario`
- `POST /auth/login` — `{ email, senha }` → `{ access_token, token_type }`
- `GET /auth/me` — Bearer JWT → `Usuario`
- `POST /simulacoes` — entrada RF01–RF04 → rascunho `Simulacao`
- `POST /simulacoes/{id}/executar` — dispara pipeline APIs + cálculo (*a implementar*)

### Auth model

JWT Bearer (HS256), senhas com bcrypt (ADR-04, ADR-06).

### ADR index

| ADR | Status | Impacto no backend |
|-----|--------|-------------------|
| 02 Monólito em camadas | Aceito | Estrutura `domain` / `application` / `infrastructure` |
| 03 Timeout APIs 10s | Aceito | `BaseHttpClient` |
| 04 Autenticação | Proposto | Rotas `/auth/*` |
| 05 APIs externas | Aceito | Clientes em `infrastructure/external` |
| 06 PostgreSQL | Aceito | Schema + Alembic |

### Open decisions

- **database-designer**: seed ANEEL, índices em `tarifas_concessionarias.concessionaria`
- **implementation**: fórmulas de payback e dimensionamento de painéis
