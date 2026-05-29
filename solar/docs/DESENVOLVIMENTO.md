# Desenvolvimento

Guia rápido para quem vai mexer no código.

---

## Pré-requisitos

- **Python 3.12** (`python3.12 --version`)
- **Docker** + **Docker Compose**
- (opcional) `gh` para criar/listar PRs

> **Por que 3.12 e não a versão mais nova do sistema?** Em distros recentes
> (3.13/3.14) o `psycopg-binary` ainda não tinha wheels publicadas no momento
> em que este MVP foi escrito; build a partir do source exige `libpq-dev`.
> 3.12 evita esse atrito. Quando wheels para versões mais novas estiverem
> disponíveis, basta atualizar.

---

## Setup completo (do zero)

```bash
git clone https://github.com/joao-pedro/solarcalc.git
cd solarcalc

# 1) Postgres em container (porta host 5433 → 5432 do container)
docker compose up -d

# 2) venv + deps
cd src/backend
python3.12 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt

# 3) Variáveis de ambiente (defaults já funcionam)
cp .env.example .env

# 4) Migrations
PYTHONPATH=. .venv/bin/alembic upgrade head

# 5) Servidor (API + frontend na mesma porta)
PYTHONPATH=. .venv/bin/uvicorn app.main:app --reload
```

Acesse:
- App: <http://127.0.0.1:8000/>
- Docs interativas (Swagger): <http://127.0.0.1:8000/docs>
- Health: <http://127.0.0.1:8000/api/v1/health>

---

## Variáveis de ambiente

Arquivo `.env` na raiz de `src/backend/` (não commitado). Padrões em
`src/backend/.env.example`:

| Variável             | Default                                                              | Para que serve                    |
| -------------------- | -------------------------------------------------------------------- | --------------------------------- |
| `DATABASE_URL`       | `postgresql+psycopg://solarcalc:solarcalc@localhost:5433/solarcalc`  | Conexão com o Postgres            |
| `JWT_SECRET`         | `change-me-in-production`                                            | Assinatura dos JWTs (auth)        |
| `JWT_EXPIRE_MINUTES` | `1440`                                                               | Duração do token                  |
| `DEBUG`              | `false`                                                              | Liga logs verbosos                |
| `GEMINI_API_KEY`     | `""`                                                                 | Chave para cotação dinâmica (futuro) |

---

## Banco de dados

### Resetar o banco

```bash
docker compose down -v          # apaga o volume
docker compose up -d
PYTHONPATH=. .venv/bin/alembic upgrade head
```

### Inspecionar tabelas

```bash
docker exec -it solarcalc-db psql -U solarcalc -d solarcalc
```

Algumas queries úteis:

```sql
-- leads capturados
SELECT nome, email, criado_em FROM usuarios ORDER BY criado_em DESC LIMIT 20;

-- últimas simulações com resultado
SELECT s.id, u.email, l.cep, dc.valor_reais,
       r.quantidade_paineis, r.potencia_sistema_kwp
FROM simulacoes s
JOIN usuarios u       ON u.id = s.usuario_id
JOIN localizacoes l   ON l.simulacao_id = s.id
JOIN dados_consumo dc ON dc.simulacao_id = s.id
JOIN resultados r     ON r.simulacao_id = s.id
ORDER BY s.realizada_em DESC LIMIT 20;
```

### Criar uma nova migration

```bash
cd src/backend
PYTHONPATH=. .venv/bin/alembic revision -m "minha mudanca"
# edite o arquivo gerado em alembic/versions/
PYTHONPATH=. .venv/bin/alembic upgrade head
```

Para gerar automaticamente a partir das models:

```bash
PYTHONPATH=. .venv/bin/alembic revision --autogenerate -m "minha mudanca"
```

(Confira o diff antes de aplicar — autogenerate erra em casos com enums e
índices únicos.)

---

## Testando manualmente os endpoints

```bash
# Health
curl http://127.0.0.1:8000/api/v1/health

# Fluxo público
curl -X POST http://127.0.0.1:8000/api/v1/simulacoes/publica \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria","email":"maria@ex.com","cep":"01310-000","valor_reais":420}'

# Reabrir resultado pelo id que veio acima
curl http://127.0.0.1:8000/api/v1/simulacoes/publica/<uuid>
```

---

## Adicionar um endpoint novo

1. Criar/atualizar schemas Pydantic em
   [`infrastructure/http/schemas.py`](../src/backend/app/infrastructure/http/schemas.py).
2. Criar/atualizar service em
   [`application/`](../src/backend/app/application/) (lógica + persistência).
3. Criar/atualizar router em
   [`infrastructure/http/routers/`](../src/backend/app/infrastructure/http/routers/).
4. Incluir o router em
   [`app/main.py`](../src/backend/app/main.py) com o prefixo `_settings.api_prefix`.

Se mexer no schema do banco: criar migration em `alembic/versions/`.

---

## Estilo e convenções

- Sem `print()` em código de produção — usar `logging` (já configurado no
  `base_client.py`).
- `Decimal` para valores monetários e métricas que vão para o banco com
  precisão fixa. Reserve `float` para HSP, eficiência etc.
- Domain errors (`DomainError`, `EntityNotFoundError`, ...) são traduzidos no
  router para `HTTPException` — services não levantam `HTTPException`.
- Frontend usa `fetch` + `async/await`. JS vanilla, sem build step.

---

## Próximos passos sugeridos

1. **Plugar Brasil API + NASA POWER** no `SimulacaoPublicaService` (já existem
   os clients prontos em `infrastructure/external/`).
2. **Calcular payback** com `custo_total` estimado.
3. **Gráfico no dashboard** comparando custo concessionária × fotovoltaico ao
   longo de 25 anos (usar Chart.js — CDN já está no `dashboard.html`).
4. **Testes automatizados** — `pytest` + `httpx` para os endpoints,
   `pytest-asyncio` para os clients externos.
5. **CI** — GitHub Actions rodando lint + testes + alembic upgrade em DB
   efêmero.
