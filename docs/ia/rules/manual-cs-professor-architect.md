# CS Professor Architect — Manual da Rule

> **Arquivo da rule:** `cs-professor-architect.mdc`  
> **Compatível com:** Claude Code · Cursor · VS Code (GitHub Copilot)  
> **Público-alvo:** Professores e alunos de Engenharia da Computação

---

## O que é esta Rule

`cs-professor-architect` é uma **rule de comportamento** para ferramentas de IA. Ela transforma o assistente em um arquiteto sênior de software, tech lead e professor de engenharia de software — simultaneamente.

A diferença em relação a uma rule técnica comum é a **dimensão pedagógica**: o assistente não entrega soluções prontas. Ele constrói sistemas em camadas, explica cada decisão antes de implementá-la e conecta o que está sendo construído ao que os alunos já estudaram no currículo.

### Rule ou Skill? Entendendo a diferença

Ferramentas como o Cursor diferenciam dois conceitos que parecem similares:

| | Rule (`.cursor/rules/`) | Skill (`.cursor/skills/<nome>/SKILL.md`) |
|---|---|---|
| **O que é** | Instrução persistente injetada no contexto | Capacidade discreta que o agente invoca pontualmente |
| **Aparece em Settings** | Não | Sim |
| **Ativação** | Automática por contexto ou `alwaysApply` | O agente decide quando usar |
| **Melhor para** | "Sempre se comporte como X" | "Saiba fazer Y quando precisar" |

**Este arquivo é uma rule.** Ele define um comportamento contínuo — o assistente deve agir como arquiteto-professor em toda conversa de desenvolvimento. Uma skill seria adequada para uma capacidade isolada e pontual, como "gerar scaffold de projeto" ou "criar diagrama ER".

---

## Capacidades da Rule

### 1. Arquitetura de sistemas com sequência didática

O assistente projeta sistemas seguindo uma sequência de sete etapas — desde a definição do objetivo até o plano de implementação por estágios. Em cada etapa, explica o que está fazendo e por que aquela etapa existe antes de avançar.

Cobre: APIs síncronas e assíncronas, autenticação e autorização, modelagem de dados, filas e eventos, cache, tratamento de falhas, logs, métricas e versionamento.

### 2. Implementação em cinco camadas de aprendizado

Todo código é construído nesta progressão:

| Camada | O que acontece |
|---|---|
| **Conceito** | Explica o problema e a categoria de solução |
| **Exemplo mínimo** | Escreve a versão mais simples que funciona |
| **Versão de produção** | Evolui para tratar restrições reais |
| **Testes** | Mostra como verificar o comportamento |
| **Próxima evolução** | Descreve o que mudaria com novos requisitos |

### 3. Code review pedagógico

Revisa código identificando primeiro o que está correto, depois os problemas por ordem de impacto. Cada problema é classificado (bug, risco de design, legibilidade, melhoria), explicado com consequência real e corrigido com um exemplo concreto. Cada correção vira um princípio reutilizável.

### 4. Debugging estruturado

Separa fatos de hipóteses. Lista candidatos à causa raiz por probabilidade. Explica como validar cada hipótese antes de propor a correção. Não afirma causa raiz sem evidência.

### 5. Mentoria adaptada ao nível do aluno

Adapta a profundidade da resposta ao estágio acadêmico detectado:

- **1º e 2º ano:** uma ideia por vez, analogias do currículo, versão ingênua antes da correta
- **3º ano:** princípios de design, trade-offs explícitos, previsão antes da resposta
- **Formandos/TCC:** tratamento de engenheiro júnior, direção sem solução, justificativa exigida

### 6. Conexão com o currículo de Engenharia da Computação

O assistente referencia o que os alunos já estudaram — estruturas de dados, algoritmos, POO, sistemas operacionais, redes, banco de dados — quando esses conceitos aparecem no código ou na arquitetura sendo construída.

### 7. Suporte full-stack integrado

Cobre Python, React e Java com orientação específica para cada stack. Quando a tarefa envolve frontend e backend juntos, define contratos de API primeiro, alinha estratégia de autenticação, paginação, serialização e explica como testar a integração ponta a ponta.

### 8. Princípio central: explicar o porquê antes do como

Antes de escrever qualquer código, o assistente declara a abordagem escolhida, o motivo da escolha, o que foi descartado e o que foi ganho com a decisão. Nenhuma abstração, padrão ou dependência é introduzida sem justificativa.

---

## Instalação

### Pré-requisito comum

O arquivo `cs-professor-architect.mdc` deve estar disponível localmente. Faça o download ou copie o conteúdo para um arquivo com esse nome antes de começar.

---

### Opção 1 — Claude Code

O Claude Code lê rules de dois locais: o diretório `.claude/commands/` do projeto ou o diretório global do usuário.

**Escopo de projeto** (recomendado para disciplinas e trabalhos):

```
meu-projeto/
└── .claude/
    └── commands/
        └── cs-professor-architect.mdc
```

Execute no terminal, dentro da pasta do projeto:

```bash
mkdir -p .claude/commands
cp cs-professor-architect.mdc .claude/commands/
```

**Escopo global** (disponível em todos os projetos):

```bash
mkdir -p ~/.claude/commands
cp cs-professor-architect.mdc ~/.claude/commands/
```

**Verificação:**

Abra o Claude Code no projeto e execute:

```
/cs-professor-architect
```

O assistente deve confirmar que está operando no modo arquiteto-professor.

---

### Opção 2 — Cursor

O Cursor lê rules de `.cursor/rules/` na raiz do projeto ou do diretório global do usuário.

**Escopo de projeto:**

```
meu-projeto/
└── .cursor/
    └── rules/
        └── cs-professor-architect.mdc
```

```bash
mkdir -p .cursor/rules
cp cs-professor-architect.mdc .cursor/rules/
```

**Escopo global** (Windows):

```
C:\Users\SEU_USUARIO\.cursor\rules\cs-professor-architect.mdc
```

```bash
# PowerShell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.cursor\rules"
Copy-Item cs-professor-architect.mdc "$env:USERPROFILE\.cursor\rules\"
```

**Ativação via interface:**

1. Abra o Cursor
2. Acesse `Settings → Rules`
3. A rule `cs-professor-architect` deve aparecer na lista
4. Confirme que está habilitada

**Ativação manual no chat:**

Se a rule não for ativada automaticamente, referencie-a diretamente no início de uma conversa:

```
@cs-professor-architect Preciso projetar uma API REST para um sistema de biblioteca.
```

> **`alwaysApply: false`** significa que a rule não é ativada automaticamente em toda conversa. O Cursor a ativa quando o contexto da tarefa corresponde à description da rule — ou quando você a referencia com `@`.

---

### Opção 3 — VS Code (GitHub Copilot)

O VS Code lê instructions de `.github/copilot-instructions.md` (workspace) ou do arquivo de instruções do usuário nas configurações do Copilot.

Como o VS Code não usa `.mdc` diretamente, o conteúdo da rule precisa ser adaptado.

**Escopo de workspace** (recomendado):

Crie o arquivo `.github/copilot-instructions.md` na raiz do projeto e cole o conteúdo da rule dentro dele, removendo o cabeçalho YAML (as linhas entre `---`):

```
meu-projeto/
└── .github/
    └── copilot-instructions.md
```

```bash
mkdir -p .github
# Copie o conteúdo da rule sem o bloco YAML do cabeçalho
```

O conteúdo de `copilot-instructions.md` deve começar diretamente em:

```
You are a senior software architect, hands-on tech lead and professor of software engineering...
```

**Escopo global** (instruções do usuário):

1. Pressione `Ctrl+Shift+P`
2. Execute `GitHub Copilot: Open User Instructions`
3. Cole o conteúdo da rule no arquivo aberto

**Verificação:**

1. Abra o Copilot Chat em **modo Agent**
2. Pergunte: `Qual é o seu papel nesta sessão?`
3. O assistente deve descrever as três funções: arquiteto, tech lead e professor

---

## Como usar a Rule nas IDEs

### Prompts de entrada recomendados

A rule identifica o tipo de tarefa automaticamente. Use linguagem natural e seja específico sobre o contexto — mencionar o ano do curso ajuda o assistente a calibrar a profundidade da resposta.

---

#### Projeto de sistema (arquitetura)

```
Sou aluno do 3º ano de Engenharia da Computação.
Preciso projetar um sistema de agendamento de consultas médicas.
O sistema terá pacientes, médicos e recepcionistas.
Por onde começo?
```

O assistente vai: identificar entidades e fronteiras, propor a arquitetura mais simples que resolve o problema, explicar cada componente, nomear os trade-offs e propor um plano de implementação por estágios.

---

#### Implementação de feature

```
Preciso implementar o endpoint POST /agendamentos em Python com Flask.
A regra é: um médico não pode ter dois agendamentos no mesmo horário.
Mostre o passo a passo desde a estrutura de pastas até os testes.
```

O assistente vai: confirmar o contrato de entrada e saída, mostrar a estrutura mínima de pastas, construir a versão mínima funcional, adicionar validação e tratamento de erros, escrever os testes e mostrar o caminho de evolução.

---

#### Code review

```
Revise este código Python que implementa autenticação JWT.
Sou aluno do 2º ano e ainda estou aprendendo boas práticas.

[cole o código aqui]
```

O assistente vai: identificar o que está correto primeiro, listar os problemas por impacto, classificar cada um, explicar a consequência real de cada problema, mostrar a versão corrigida e transformar cada correção em um princípio que o aluno pode carregar para outros projetos.

---

#### Debugging

```
Meu endpoint retorna 200 mas não salva no banco.
Não há mensagem de erro no terminal.
O código é este:

[cole o código aqui]
```

O assistente vai: descrever o sintoma com precisão, listar as hipóteses mais prováveis, explicar como validar cada uma e propor a menor correção possível após identificar a causa raiz.

---

#### Explicação de conceito

```
Qual a diferença entre autenticação e autorização?
Me dê um exemplo em código Python com Flask.
```

O assistente vai: explicar o conceito conectando-o ao que o aluno já estudou, mostrar o exemplo mais simples possível e depois evoluí-lo para uma versão mais próxima do uso real.

---

#### Trabalho de conclusão de curso (TCC)

```
Estou no último ano e quero construir uma plataforma de monitoramento
de qualidade de código para repositórios GitHub.
Analise minha proposta de arquitetura:

[descreva ou cole o diagrama/texto aqui]
```

Para alunos em fase final, o assistente trata o estudante como engenheiro júnior: revisa o raciocínio, questiona as escolhas sem oferecer a solução diretamente e exige justificativas antes de validar uma direção.

---

### Dicas de uso

**Informe o ano do curso.** A rule adapta a profundidade e o vocabulário ao estágio acadêmico. Um aluno do 1º ano recebe analogias e progressão lenta. Um formando recebe feedback de tech lead.

**Peça a construção em etapas.** Se o assistente entregar uma solução completa sem sequência, peça explicitamente: `"Construa em etapas, explicando cada decisão antes de avançar."`

**Peça conexão com o currículo.** Se quiser que o assistente conecte o conteúdo ao que você estudou: `"Conecte isso com o que aprendi em Banco de Dados 2."`

**Use para revisão antes de entregar.** Cole seu código com o contexto `"Revise como um tech lead revisaria um pull request de um júnior."` para receber feedback estruturado antes de submeter trabalhos.

---

## Localização dos arquivos por ferramenta

```
Windows — Caminhos de instalação
──────────────────────────────────────────────────────────────────
Claude Code
  Projeto:  <projeto>\.claude\commands\cs-professor-architect.mdc
  Global:   C:\Users\SEU_USUARIO\.claude\commands\cs-professor-architect.mdc

Cursor
  Projeto:  <projeto>\.cursor\rules\cs-professor-architect.mdc
  Global:   C:\Users\SEU_USUARIO\.cursor\rules\cs-professor-architect.mdc

VS Code
  Workspace: <projeto>\.github\copilot-instructions.md
  Global:    via Ctrl+Shift+P → "GitHub Copilot: Open User Instructions"
──────────────────────────────────────────────────────────────────
```

---

## Referências

- Documentação Claude Code — Custom commands: [docs.anthropic.com/en/docs/claude-code/slash-commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- Documentação Cursor — Rules: [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules)
- Documentação VS Code — Copilot instructions: [code.visualstudio.com/docs/copilot/copilot-customization](https://code.visualstudio.com/docs/copilot/copilot-customization)
