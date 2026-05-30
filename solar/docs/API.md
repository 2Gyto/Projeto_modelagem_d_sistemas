# API

Todos os endpoints ficam sob o prefixo `/api/v1`. Quando a API estiver
rodando em `http://127.0.0.1:8000`, a documentação interativa do FastAPI fica
em <http://127.0.0.1:8000/docs>.

---

## Convenções

- Corpo de requisição e resposta sempre em `application/json`.
- Erros seguem o padrão FastAPI: `{ "detail": "mensagem em português" }`.
- Valores monetários e numéricos são serializados como **string** quando vêm
  de `Decimal` (precaução contra perda de precisão em JSON). Converta para
  número no cliente.

---

## Códigos de status comuns

| Código | Significado                                                       |
| ------ | ----------------------------------------------------------------- |
| 200    | OK (GET com sucesso)                                              |
| 201    | Created (POST que criou recurso)                                  |
| 401    | Não autenticado (rotas que exigem JWT)                            |
| 404    | Recurso não encontrado                                            |
| 409    | Conflito (ex.: e-mail já registrado em `/auth/register`)          |
| 422    | Erro de validação (Pydantic) ou erro de domínio (`DomainError`)   |
| 503    | Falha em API externa (`ExternalApiError`)                         |

---

## Sistema

### `GET /api/v1/health`

Liveness simples. Útil para health checks de orquestrador.

**Resposta 200**
```json
{ "status": "ok", "app": "SolarCalc API" }
```

---

## Fluxo público (MVP, **sem autenticação**)

### `POST /api/v1/simulacoes/publica`

Cria/atualiza um lead, persiste a simulação, executa o cálculo e devolve o
resultado.

**Request**
```json
{
  "nome": "João Teste",
  "email": "joao.teste@example.com",
  "cep": "01310-000",
  "valor_reais": 350
}
```

| Campo         | Tipo            | Regras                                |
| ------------- | --------------- | ------------------------------------- |
| `nome`        | string          | 2–100 caracteres                      |
| `email`       | string (email)  | validado por Pydantic                 |
| `cep`         | string          | 8 ou 9 caracteres (aceita com hífen)  |
| `valor_reais` | número decimal  | > 0                                   |

**Resposta 201**
```json
{
  "simulacao_id": "8944df5b-8249-48f7-b08e-9155e6196719",
  "nome": "João Teste",
  "email": "joao.teste@example.com",
  "cep": "01310-000",
  "valor_reais": "350",
  "consumo_kwh_mes": "411.76",
  "quantidade_paineis": 7,
  "potencia_sistema_kwp": "3.85",
  "geracao_total_kwh_mes": "462.00",
  "economia_mensal_reais": "350.00"
}
```

Comportamento do upsert: se o `email` já existir em `usuarios`, o registro é
reaproveitado (e o `nome` é atualizado se mudou). Se não existir, cria um
usuário sem senha (`senha_hash = NULL`).

### `GET /api/v1/simulacoes/publica/{simulacao_id}`

Reabre o resultado de uma simulação pública pelo `simulacao_id` (UUID).

**Resposta 200** — mesmo formato do POST.

**Erros**
- `404` — simulação não encontrada ou sem resultado associado.

---

## Autenticação (opcional, fluxo avançado)

Existe para o caso de o usuário querer histórico próprio. Não é usado no fluxo
do MVP descrito acima.

### `POST /api/v1/auth/register`

**Request**
```json
{ "nome": "Maria", "email": "maria@ex.com", "senha": "umaSenhaForte" }
```

**Resposta 201**
```json
{ "id": "uuid", "nome": "Maria", "email": "maria@ex.com", "criado_em": "2026-05-29T13:00:00Z" }
```

**Erros**
- `409` — `EmailAlreadyRegisteredError`.

### `POST /api/v1/auth/login`

**Request**
```json
{ "email": "maria@ex.com", "senha": "umaSenhaForte" }
```

**Resposta 200**
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

**Erros**
- `401` — `InvalidCredentialsError`.

### `GET /api/v1/auth/me`

Header: `Authorization: Bearer <token>`.

**Resposta 200** — mesmo `UsuarioResponse` do `/register`.

---

## Simulações autenticadas

Todas exigem `Authorization: Bearer <token>`.

### `POST /api/v1/simulacoes`

Cria rascunho com dados completos (telhado + conexão). Não roda cálculo
ainda — para isso usa-se o `/executar` (placeholder).

**Request**
```json
{
  "consumo_kwh": 320,
  "valor_reais": null,
  "tipo_entrada": "KWH",
  "cep": "01310-000",
  "cidade": "São Paulo",
  "area_m2": 25.5,
  "orientacao": "NORTE",
  "tipo_conexao": "BIFASICA"
}
```

Regras de domínio:
- `consumo_kwh` **ou** `valor_reais` precisa estar presente (`DomainError`).
- `tipo_entrada` ∈ `{KWH, REAIS}`.
- `orientacao` ∈ `{NORTE, SUL, LESTE, OESTE}`.
- `tipo_conexao` ∈ `{MONOFASICA, BIFASICA, TRIFASICA}`.

### `GET /api/v1/simulacoes`
Lista simulações do usuário logado, ordem decrescente por `realizada_em`.

### `GET /api/v1/simulacoes/{id}`
Busca uma simulação do usuário. 404 se não pertence ou não existe.

### `POST /api/v1/simulacoes/{id}/executar`
**Placeholder** — retorna `501 Not Implemented`. Será o ponto que integra
Brasil API + NASA POWER + Gemini.

---

## Erros e payloads de exemplo

### 422 — Pydantic

```json
{
  "detail": [
    {"loc": ["body", "valor_reais"], "msg": "ensure this value is greater than 0", "type": "value_error.number.not_gt"}
  ]
}
```

### 422 — Domínio

```json
{ "detail": "Informe consumo em kWh ou valor em reais (RB01)." }
```

### 404

```json
{ "detail": "Simulação não encontrada." }
```

### 503 — externa

```json
{ "detail": "Serviço temporariamente indisponível. Tente novamente mais tarde.", "api": "Brasil API" }
```
