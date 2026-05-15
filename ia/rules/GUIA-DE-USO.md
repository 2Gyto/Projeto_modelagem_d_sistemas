# Guia de uso — Pipeline de 7 Skills

Este guia mostra como instalar, ativar e encadear as 7 skills no Cursor. Inclui exemplos reais de chamadas para cada estágio.

---

## Instalação

1. Na raiz do seu projeto, crie a pasta `.cursor/rules/` se ela ainda não existir.
2. Copie os 7 arquivos `.mdc` para dentro dela.

```
meu-projeto/
├── .cursor/
│   └── rules/
│       ├── 01-requirements-analyst.mdc
│       ├── 02-senior-stack-architect.mdc
│       ├── 03-database-designer.mdc
│       ├── 04-ui-ux-designer.mdc
│       ├── 05-implementation-engineer.mdc
│       ├── 06-qa-engineer.mdc
│       └── 07-docs-and-ops.mdc
├── context/          ← crie esta pasta para os artefatos de handoff
└── src/
```

3. Crie também a pasta `context/` na raiz. É onde cada skill salva seu artefato de saída para a próxima consumir.

> **Nota:** as skills têm `alwaysApply: false`, então o Cursor as carrega seletivamente com base no que você escreve. Você não precisa ativá-las manualmente — basta escrever uma mensagem que corresponda ao contexto da skill.

---

## Como as skills se ativam

O Cursor lê o campo `description` de cada `.mdc` e decide qual carregar com base na sua mensagem. As skills se ativam por:

- **palavras-chave** — "requisitos", "arquitetura", "schema", "implementar", "QA", "deploy"
- **contexto** — se você referenciar um documento com `@context/02-architecture.md`, o Cursor entende que você está no estágio relacionado
- **chamada explícita** — você pode sempre chamar pelo nome: `"use a skill 03-database-designer"`

---

## Fluxo completo do pipeline

```
01 Requisitos
    ↓
02 Arquitetura
    ↓
03 Database ←→ 04 UI/UX   (paralelo)
         ↓
    05 Implementação
         ↓
    06 QA
         ↓
    07 Docs e Ops
```

Cada estágio termina com uma instrução de próximo passo. A skill diz exatamente qual arquivo salvar e qual prompt usar para continuar.

---

## Estágio 01 — Levantamento de Requisitos

**Quando usar:** início de um projeto ou feature. Você tem uma ideia, um problema ou uma solicitação de stakeholder, mas ainda não tem especificação técnica.

**Exemplos de chamada:**

```
Quero construir um sistema de agendamento de consultas para uma clínica veterinária.
```

```
Preciso levantar os requisitos para uma feature de notificações em tempo real
no nosso app de entregas. Os clientes reclamam que não sabem onde está o pedido.
```

```
Temos uma solicitação do cliente para adicionar um módulo de relatórios financeiros.
Ainda não sei exatamente o que ele quer. Me ajuda a estruturar os requisitos.
```

```
Use a skill 01-requirements-analyst para documentar o escopo do sistema de login
com suporte a OAuth que precisamos construir para o TCC.
```

**O que a skill produz:**

Um documento estruturado com: Context, Actors, Functional Requirements (FR-01, FR-02...), Non-Functional Requirements (NFR-01...), Business Rules, Constraints, Out of Scope e Open Questions. Mais um Architecture Handoff Summary no final.

**Onde salvar o output:**

```
context/01-requirements.md
```

---

## Estágio 02 — Arquitetura de Sistema

**Quando usar:** depois que os requisitos estão documentados. Você quer projetar a solução técnica com trade-offs explícitos e decisões registradas.

**Exemplos de chamada:**

```
@context/01-requirements.md

Revise o documento de requisitos acima e projete a arquitetura do sistema
usando a skill 02-senior-stack-architect.
```

```
@context/01-requirements.md

Temos os requisitos do sistema de agendamento. Preciso de uma arquitetura
que suporte 500 usuários simultâneos com tempo de resposta abaixo de 300ms.
```

```
Sem requisitos formais ainda, mas preciso de uma arquitetura para um sistema
de chat em tempo real com Python no backend e React no frontend.
Use a skill 02-senior-stack-architect.
```

**O que a skill produz:**

Component map, API contracts, ADRs (Architecture Decision Records) para cada decisão significativa, data entities and access patterns, auth model, non-functional targets e infrastructure sketch.

**Onde salvar o output:**

```
context/02-architecture.md
```

---

## Estágio 03 — Design de Banco de Dados

**Quando usar:** depois da arquitetura. Você quer transformar as entidades e os access patterns em um schema concreto, com índices, constraints e plano de migration.

> Pode rodar em paralelo com o estágio 04.

**Exemplos de chamada:**

```
@context/01-requirements.md @context/02-architecture.md

Revise os documentos acima e projete o modelo de dados
usando a skill 03-database-designer.
```

```
@context/02-architecture.md

A arquitetura definiu as entidades User, Appointment, Vet e Pet.
Preciso do schema PostgreSQL completo com índices justificados e as migrations.
```

```
Tenho um sistema com alta taxa de leitura em relatórios e escrita eventual
em eventos. Use a skill 03-database-designer para me ajudar a decidir
entre normalizar ou desnormalizar a tabela de eventos.
```

**O que a skill produz:**

Schema completo por entidade (colunas, tipos, constraints, índices com justificativa por access pattern), technology selection justificada, migration plan e performance checklist.

**Onde salvar o output:**

```
context/03-database.md
```

---

## Estágio 04 — Design de UI/UX

**Quando usar:** em paralelo com o estágio 03. Você quer transformar os contratos de API e os user journeys em especificações de tela com todos os estados.

> Pode rodar em paralelo com o estágio 03.

**Exemplos de chamada:**

```
@context/01-requirements.md @context/02-architecture.md

Revise os documentos acima e projete o layout e os fluxos de tela
usando a skill 04-ui-ux-designer.
```

```
@context/02-architecture.md

Os contratos de API estão definidos. Preciso das especificações de tela
para o fluxo de agendamento: listagem de horários, seleção, confirmação e
tela de sucesso. Inclua todos os estados de loading, erro e vazio.
```

```
Preciso do design system e da hierarquia de componentes para um dashboard
administrativo com React. Use a skill 04-ui-ux-designer.
```

**O que a skill produz:**

Screen inventory, component hierarchy, screen specification por tela (com estados loading/empty/error/success), design tokens completos e accessibility checklist.

**Onde salvar o output:**

```
context/04-ui-ux.md
```

---

## Estágio 05 — Implementação

**Quando usar:** depois que os estágios 03 e 04 estão completos. Você quer transformar toda a especificação em código pronto para produção.

**Exemplos de chamada:**

```
@context/01-requirements.md @context/02-architecture.md @context/03-database.md @context/04-ui-ux.md

Revise todos os documentos acima e inicie a implementação
usando a skill 05-implementation-engineer.
```

```
@context/02-architecture.md @context/03-database.md

Implemente o backend: migrations, repositories, service layer e handlers
para o módulo de agendamentos. Stack: Python com FastAPI.
Use a skill 05-implementation-engineer.
```

```
@context/04-ui-ux.md

Implemente os componentes React para o fluxo de agendamento conforme
a spec de UI. Inclua todos os estados e os testes de componente.
Use a skill 05-implementation-engineer.
```

**O que a skill produz:**

Estrutura de módulos e pastas antes do primeiro arquivo, código por camada (data → service → API → UI), testes unitários e de integração e deviation log documentando qualquer desvio da spec.

**Onde salvar o output:**

```
context/05-implementation.md   ← contém o deviation log
```

---

## Estágio 06 — QA e Testes

**Quando usar:** depois que a implementação está completa. Você quer validar tudo contra os requisitos originais e emitir um veredicto GO / NO-GO.

**Exemplos de chamada:**

```
@context/01-requirements.md @context/02-architecture.md @context/03-database.md @context/04-ui-ux.md @context/05-implementation.md

Revise todos os documentos acima e execute o plano de QA
usando a skill 06-qa-engineer.
```

```
@context/01-requirements.md @context/05-implementation.md

Preciso da matriz de rastreabilidade e dos casos de teste para os
requisitos funcionais FR-01 a FR-07. Use a skill 06-qa-engineer.
```

```
@context/02-architecture.md @context/05-implementation.md

O deviation log do estágio 05 mostra 3 desvios da spec. Preciso de
casos de teste específicos para cobrir cada um deles.
Use a skill 06-qa-engineer.
```

**O que a skill produz:**

Requirements traceability matrix, test plan por categoria (functional, integration, performance, security, UI/UX), casos de teste no formato TC-N e quality gate report com veredicto GO / NO-GO / CONDITIONAL GO.

**Onde salvar o output:**

```
context/06-qa.md
```

---

## Estágio 07 — Documentação e Operações

**Quando usar:** depois do quality gate aprovado. Você quer documentar o sistema e preparar tudo para ir para produção.

**Exemplos de chamada:**

```
@context/01-requirements.md @context/02-architecture.md @context/03-database.md @context/04-ui-ux.md @context/05-implementation.md @context/06-qa.md

Revise todos os documentos acima e produza a documentação técnica
e o plano operacional usando a skill 07-docs-and-ops.
```

```
@context/02-architecture.md @context/06-qa.md

O QA foi aprovado. Preciso dos runbooks para os cenários de falha
identificados na arquitetura e da estratégia de observabilidade.
Use a skill 07-docs-and-ops.
```

```
@context/01-requirements.md @context/07-docs-and-ops.md

Preciso fechar o pipeline com a tabela de rastreabilidade de requisitos —
confirmando quais FRs e NFRs foram entregues, documentados e instrumentados.
```

**O que a skill produz:**

README, API docs, configuration reference, deployment procedure com verification steps, rollback procedure, observability strategy (logs/metrics/traces), alerting rules ligadas aos NFRs, runbooks por cenário de falha, release checklist e requirements traceability closure.

**Onde salvar o output:**

```
context/07-docs-and-ops.md
```

---

## Como chamar uma skill explicitamente

Se o Cursor não ativar a skill automaticamente, force a chamada pelo nome:

```
Use a skill 01-requirements-analyst para levantar os requisitos do módulo X.
```

```
Aja como a skill 03-database-designer e revise este schema.
```

```
Preciso do estágio 05 do pipeline: implementação completa do módulo de auth.
```

---

## Usando apenas uma skill isolada

As skills funcionam independentemente do pipeline. Você pode usá-las em qualquer momento sem seguir a sequência completa:

```
Use a skill 02-senior-stack-architect para revisar esta decisão de arquitetura:
estou pensando em usar WebSockets para o chat, mas não sei se vale a complexidade.
```

```
Use a skill 06-qa-engineer para me ajudar a escrever casos de teste para
este endpoint de pagamento. Não temos documento de requisitos formal.
```

```
Tenho este schema de banco de dados que herdei. Use a skill 03-database-designer
para auditá-lo e identificar problemas de performance e integridade.
```

---

## Referência rápida — pasta `context/` ao final do pipeline

```
context/
├── 01-requirements.md     ← o que foi acordado
├── 02-architecture.md     ← como foi projetado (inclui ADRs)
├── 03-database.md         ← como os dados são modelados
├── 04-ui-ux.md            ← como parece e como se comporta
├── 05-implementation.md   ← o que foi construído e o que desviou
├── 06-qa.md               ← o que foi validado e o que foi encontrado
└── 07-docs-and-ops.md     ← como operar e evoluir
```

Esta pasta é o audit trail completo da feature. Se alguém entrar no projeto depois, tem toda a história das decisões em um único lugar.

---

## Iniciando uma nova feature

Ao terminar um ciclo e começar uma nova feature, volte ao estágio 01:

```
Quero levantar os requisitos para [nome da próxima feature].
Use a skill 01-requirements-analyst.
```

Os arquivos da feature anterior ficam em `context/`. Para a nova feature, você pode criar uma subpasta:

```
context/
├── feature-agendamento/
│   ├── 01-requirements.md
│   └── ...
└── feature-notificacoes/
    ├── 01-requirements.md
    └── ...
```
