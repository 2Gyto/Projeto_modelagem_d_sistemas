# Material UI MCP — Guia de Instalação e Uso

> **Biblioteca:** Material UI v9 (`@mui/material`)  
> **Servidor MCP:** `@mui/mcp@latest` (oficial)  
> **Compatível com:** Claude Code · Cursor · VS Code (GitHub Copilot)  
> **Sistema operacional:** Windows (nativo)

---

## Por que instalar o MUI MCP

Sem o MCP, o assistente responde sobre Material UI a partir do treinamento — que pode estar desatualizado, citar props inexistentes ou linkar para páginas que não existem.

Com o MUI MCP instalado, o assistente:

- consulta a documentação oficial real antes de responder
- cita fontes verificáveis com links funcionais
- usa código do registry de componentes publicado pelo MUI
- nunca inventa nomes de props ou versões de componentes

---

## Pré-requisitos

- **Node.js 18 ou superior** — [nodejs.org](https://nodejs.org)  
  Verifique: `node --version`
- Uma das ferramentas: Claude Code, Cursor ou VS Code com GitHub Copilot

---

## Instalação

### 1. Claude Code

Execute no terminal. Escolha o escopo conforme a necessidade:

```bash
# Escopo do projeto atual (recomendado para trabalhos e disciplinas)
claude mcp add mui-mcp -- npx -y @mui/mcp@latest

# Escopo global (disponível em todos os projetos da máquina)
claude mcp add mui-mcp -s user -- npx -y @mui/mcp@latest
```

**Verificação:**

```bash
claude mcp list
```

O servidor `mui-mcp` deve aparecer como ativo. Dentro do Claude Code, use `/mcp` para confirmar o status em tempo real.

---

### 2. Cursor

Crie ou edite o arquivo de configuração MCP do projeto:

```
meu-projeto/
└── .cursor/
    └── mcp.json
```

Conteúdo do arquivo:

```json
{
  "mcpServers": {
    "mui-mcp": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@mui/mcp@latest"]
    }
  }
}
```

Para configuração global (todos os projetos), crie o arquivo em:

```
C:\Users\SEU_USUARIO\.cursor\mcp.json
```

**Verificação:**

1. Abra o Cursor
2. Acesse `Settings → Tools & MCP`
3. O servidor `mui-mcp` deve aparecer com indicador verde

---

### 3. VS Code (GitHub Copilot)

Crie ou edite `.vscode/mcp.json` na raiz do projeto:

```json
{
  "servers": {
    "mui-mcp": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@mui/mcp@latest"]
    }
  }
}
```

Adicione também ao `settings.json` do VS Code (`Ctrl+Shift+P → Open User Settings JSON`):

```json
"chat.mcp.enabled": true,
"chat.mcp.discovery.enabled": true
```

> **Lembre:** o VS Code usa `"servers"` como chave raiz, não `"mcpServers"`. Cursor e Claude Code usam `"mcpServers"`. Trocar essa chave é o erro mais comum.

**Verificação:**

1. Pressione `Ctrl+Shift+P`
2. Execute `MCP: List Servers`
3. O servidor `mui-mcp` deve aparecer com status `Connected`

---

## Rule de ativação (obrigatória nos três clientes)

Instalar o MCP não garante que o assistente o consulte automaticamente. Crie uma rule que instrui o comportamento explicitamente.

Crie o arquivo no caminho correto para cada ferramenta:

| Ferramenta | Caminho da rule |
|---|---|
| Claude Code | `.claude/rules/mui.md` |
| Cursor | `.cursor/rules/mui.md` |
| VS Code | `.github/instructions/mui.md` |

Conteúdo do arquivo (igual para os três):

```markdown
## Use o servidor mui-mcp para qualquer pergunta sobre Material UI ou MUI

1. Chame a ferramenta "useMuiDocs" para buscar a documentação do pacote relevante
2. Chame a ferramenta "fetchDocs" para buscar documentação adicional usando apenas
   as URLs presentes no conteúdo retornado
3. Repita os passos 1 e 2 até ter toda a documentação relevante para a pergunta
4. Responda usando apenas o conteúdo buscado — nunca a partir da memória de treinamento
```

---

## Como usar nas IDEs

### Estrutura de prompt recomendada

Sempre informe a versão do MUI e a stack utilizada. O assistente vai buscar a documentação correta antes de responder.

```
Stack: React 18 + Material UI v9 + TypeScript
[sua pergunta aqui]
```

---

### Exemplos por tipo de tarefa

---

#### Componente simples

```
Stack: React + MUI v9

Crie um botão de login com:
- ícone de cadeado à esquerda
- estado de loading ao clicar
- variante contained com cor primary
```

Resposta esperada: o assistente consulta o MCP, retorna o código com `Button`, `CircularProgress`
e `LockOutlinedIcon` usando a API correta do MUI v9.

---

#### Formulário completo

```
Stack: React + MUI v9 + React Hook Form

Crie um formulário de cadastro de usuário com:
- campos: nome, email, senha, confirmação de senha
- validação inline nos campos
- botão de submit com loading state
- feedback de erro e sucesso com Snackbar
```

---

#### Layout de página

```
Stack: React + MUI v9

Crie um layout de dashboard com:
- Drawer lateral colapsável com menu de navegação
- AppBar com título e avatar do usuário
- área de conteúdo principal com Grid responsivo
- funciona em mobile (drawer vira bottom navigation)
```

---

#### Tema customizado

```
Stack: React + MUI v9

Crie um tema MUI customizado com:
- paleta de cores: primária #1A237E (azul escuro), secundária #FF6F00 (âmbar)
- tipografia: Roboto para corpo, Playfair Display para títulos
- border-radius padrão de 8px em todos os componentes
- modo escuro ativado por padrão
Mostre como aplicar o tema na raiz da aplicação.
```

---

#### Tabela de dados

```
Stack: React + MUI v9

Crie uma tabela de alunos com:
- colunas: nome, matrícula, curso, situação (ativo/inativo)
- ordenação por coluna ao clicar no cabeçalho
- paginação com 10 itens por página
- chip colorido para a coluna situação (verde/vermelho)
- campo de busca acima da tabela
```

---

#### Revisão de componente existente

```
Stack: React + MUI v9

Revise este componente. Verifique se as props, importações e a API
estão corretos para o MUI v9. Aponte o que mudou da v5 para v9.

[cole o componente aqui]
```

---

### Dicas de uso

**Especifique a versão.** O MUI mudou APIs significativamente entre v5 e v9. Sem especificar, o assistente pode usar a versão errada mesmo com o MCP ativo.

**Use o MCP para debug.** Se um componente não funciona como esperado, peça ao assistente para verificar na documentação oficial:

```
Verifique na documentação do MUI v9 quais são as props aceitas pelo componente
TextField no modo multiline. Meu componente está apresentando [descreva o problema].
```

**Peça exemplos com acessibilidade.** O MUI tem suporte nativo a ARIA. Explore isso:

```
Crie um Dialog de confirmação de exclusão com suporte completo
a acessibilidade (aria-labelledby, aria-describedby, foco gerenciado).
```

**Combine com a rule cs-professor-architect.** Se você instalou a rule do arquiteto-professor, use as duas juntas:

```
Sou aluno do 3º ano. Usando MUI v9, explique o que é o sistema de Grid
do Material UI e como ele se diferencia do Flexbox puro.
Em seguida, crie um layout de três colunas responsivo que colapsa
para uma coluna em mobile.
```

---

## Diagnóstico de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| MCP não aparece na lista | Chave raiz errada no JSON | `"mcpServers"` (Cursor/Claude Code) ou `"servers"` (VS Code) |
| Servidor trava ao iniciar | Falta do `cmd /c` no Windows | Use `"command": "cmd"` e `"args": ["/c", "npx", ...]` |
| Assistente ignora o MCP | Rule de ativação ausente | Crie o arquivo `.md` de instrução descrito neste guia |
| Respostas desatualizadas | MCP não está sendo consultado | Pergunte explicitamente: `"Busque na documentação do MUI v9..."` |
| Erro de conexão | Node.js ausente ou desatualizado | Execute `node --version` — precisa ser 18 ou superior |

**Debug via MCP Inspector:**

```bash
npx @modelcontextprotocol/inspector
```

Acesse `http://127.0.0.1:6274`, configure:

- Transport type: `Stdio`
- Command: `npx`
- Arguments: `-y @mui/mcp@latest`

Clique em Connect. A lista de ferramentas disponíveis deve aparecer.

---

## Resumo: localização dos arquivos

```
Windows — Caminhos de configuração
──────────────────────────────────────────────────────────────────
Claude Code
  MCP:   instalado via CLI (claude mcp add)
  Rule:  <projeto>\.claude\rules\mui.md

Cursor
  MCP:   <projeto>\.cursor\mcp.json
         C:\Users\SEU_USUARIO\.cursor\mcp.json  (global)
  Rule:  <projeto>\.cursor\rules\mui.md

VS Code
  MCP:   <projeto>\.vscode\mcp.json
  Rule:  <projeto>\.github\instructions\mui.md
  Config: settings.json → chat.mcp.enabled: true
──────────────────────────────────────────────────────────────────
```

---

## Referências

- Documentação oficial MUI MCP: [mui.com/material-ui/getting-started/mcp](https://mui.com/material-ui/getting-started/mcp/)
- Documentação MUI v9: [mui.com/material-ui](https://mui.com/material-ui/getting-started/)
- llms.txt do MUI (contexto estático): [mui.com/material-ui/llms.txt](https://mui.com/material-ui/llms.txt)
- MCP Inspector: [modelcontextprotocol.io/docs/tools/inspector](https://modelcontextprotocol.io/docs/tools/inspector)
