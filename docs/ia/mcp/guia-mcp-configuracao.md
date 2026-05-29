# Guia de Configuração MCP — Windows

> **Para:** Alunos de Engenharia da Computação  
> **Ferramentas cobertas:** Claude Code · Cursor · VS Code (GitHub Copilot)  
> **Sistema operacional:** Windows (nativo, não WSL)

---

## O que é MCP

Model Context Protocol (MCP) é um protocolo aberto que permite que ferramentas de IA se conectem a serviços externos: bancos de dados, APIs, sistemas de arquivos e outros. Você escreve a configuração uma vez. A IA usa os servidores configurados para consultar dados reais durante a conversa.

Este guia configura quatro servidores:

| Servidor | O que faz |
|---|---|
| **GitHub** | Lê issues, PRs, repositórios e código |
| **MySQL** | Consulta bancos MySQL locais |
| **SQL Server** | Consulta bancos SQL Server locais |
| **REST API** | Faz requisições HTTP a qualquer API pública ou privada |

---

## Pré-requisitos

Instale antes de começar:

- **Node.js 18 ou superior** — [nodejs.org](https://nodejs.org)  
  Verifique: `node --version`

- **Git** — [git-scm.com](https://git-scm.com)

- **MySQL Server** rodando na porta `3306`

- **SQL Server** (Express ou full) rodando na porta `1433`

- **GitHub Personal Access Token (PAT)**  
  Acesse: `github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)`  
  Escopos necessários: `repo`, `read:org`, `read:user`

---

## Atenção: credenciais em arquivos de configuração

Nunca versione arquivos com senhas ou tokens reais.

Adicione ao seu `.gitignore`:

```
.mcp.json
.cursor/mcp.json
.vscode/mcp.json
```

Use sempre usuários de banco com permissões mínimas. Veja a seção de segurança ao final deste guia.

---

## Diferenças entre os clientes

Cada ferramenta lê o arquivo de configuração de um local diferente e usa uma chave raiz diferente. Essa é a principal fonte de erros.

| Cliente | Arquivo | Chave raiz | Escopo |
|---|---|---|---|
| Claude Code | `.mcp.json` | `mcpServers` | Projeto ou global (`~\.mcp.json`) |
| Cursor | `.cursor\mcp.json` | `mcpServers` | Projeto ou global (`~\.cursor\mcp.json`) |
| VS Code | `.vscode\mcp.json` | **`servers`** | Workspace ou global |

> **Atenção:** o VS Code usa `"servers"` como chave raiz. Cursor e Claude Code usam `"mcpServers"`. Trocar as chaves é o erro mais comum ao copiar configurações entre ferramentas.

---

## 1. Claude Code

### Instalação

```bash
npm install -g @anthropic-ai/claude-code
```

Verifique: `claude --version`

### Arquivo de configuração

Crie o arquivo `.mcp.json` na raiz do seu projeto. Para configuração global (todos os projetos), crie em `C:\Users\SEU_USUARIO\.mcp.json`.

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer SEU_GITHUB_PAT_AQUI"
      }
    },
    "mysql": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "mcp_user",
        "MYSQL_PASS": "SUA_SENHA",
        "MYSQL_DB": "nome_do_banco",
        "ALLOW_INSERT_OPERATION": "false",
        "ALLOW_UPDATE_OPERATION": "false",
        "ALLOW_DELETE_OPERATION": "false"
      }
    },
    "sqlserver": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bilims/mcp-sqlserver"],
      "env": {
        "SQLSERVER_HOST": "localhost",
        "SQLSERVER_PORT": "1433",
        "SQLSERVER_USER": "SEU_USUARIO",
        "SQLSERVER_PASSWORD": "SUA_SENHA",
        "SQLSERVER_DATABASE": "nome_do_banco",
        "SQLSERVER_ENCRYPT": "false",
        "SQLSERVER_TRUST_CERT": "true"
      }
    },
    "rest-api": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-fetch-server"],
      "env": {
        "DEFAULT_LIMIT": "50000"
      }
    }
  }
}
```

> **Por que `cmd /c`?** No Windows nativo, o `npx` não é um executável direto — é um script. O Claude Code não consegue executá-lo sem o wrapper `cmd /c`. Sem ele, o servidor não inicia e nenhuma mensagem de erro aparece.

### Como verificar se está funcionando

Abra o terminal na pasta do projeto e execute:

```bash
claude mcp list
```

O retorno deve listar `github`, `mysql`, `sqlserver` e `rest-api` com status ativo.

Dentro do Claude Code, digite `/mcp` para ver o status dos servidores em tempo real.

### Escopos de configuração

```bash
# Disponível apenas no projeto atual (padrão)
# Coloque .mcp.json na raiz do projeto

# Disponível em todos os projetos do usuário
# Coloque .mcp.json em C:\Users\SEU_USUARIO\.mcp.json
```

---

## 2. Cursor

### Pré-requisito

Instale o Cursor em [cursor.com](https://cursor.com).

### Arquivo de configuração

**Escopo de projeto** (recomendado para aulas): crie a pasta `.cursor` na raiz do projeto e dentro dela o arquivo `mcp.json`.

```
meu-projeto/
└── .cursor/
    └── mcp.json
```

**Escopo global** (todos os projetos): crie o arquivo em `C:\Users\SEU_USUARIO\.cursor\mcp.json`.

O conteúdo é idêntico ao do Claude Code — a chave raiz é `mcpServers`:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer SEU_GITHUB_PAT_AQUI"
      }
    },
    "mysql": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "mcp_user",
        "MYSQL_PASS": "SUA_SENHA",
        "MYSQL_DB": "nome_do_banco",
        "ALLOW_INSERT_OPERATION": "false",
        "ALLOW_UPDATE_OPERATION": "false",
        "ALLOW_DELETE_OPERATION": "false"
      }
    },
    "sqlserver": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bilims/mcp-sqlserver"],
      "env": {
        "SQLSERVER_HOST": "localhost",
        "SQLSERVER_PORT": "1433",
        "SQLSERVER_USER": "SEU_USUARIO",
        "SQLSERVER_PASSWORD": "SUA_SENHA",
        "SQLSERVER_DATABASE": "nome_do_banco",
        "SQLSERVER_ENCRYPT": "false",
        "SQLSERVER_TRUST_CERT": "true"
      }
    },
    "rest-api": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-fetch-server"],
      "env": {
        "DEFAULT_LIMIT": "50000"
      }
    }
  }
}
```

### Como verificar se está funcionando

1. Abra o Cursor
2. Acesse `Settings → Tools & MCP`
3. Os quatro servidores devem aparecer com indicador verde

Alternativamente, abra o chat do Cursor e pergunte: `"Liste as ferramentas que você tem disponíveis"`.

> **Limite do Cursor:** o agente suporta até 40 ferramentas ativas simultaneamente. Se você tiver muitos servidores MCP, desative os que não usa em `Settings → Tools & MCP`.

---

## 3. VS Code (GitHub Copilot)

### Pré-requisitos

- VS Code 1.99 ou superior
- Extensão **GitHub Copilot** instalada e ativa
- Conta GitHub com acesso ao Copilot (plano Free inclui MCP)

> **Importante:** no VS Code, o MCP funciona exclusivamente no **modo Agent** do Copilot Chat. Não funciona no modo Ask ou no Inline Chat.

### Diferença crítica

O VS Code usa `"servers"` como chave raiz, **não** `"mcpServers"`. Se você copiar a config do Cursor sem alterar essa chave, os servidores não carregam e nenhum erro aparece.

### Arquivo de configuração

**Escopo de workspace** (recomendado para projetos de aula): crie `.vscode/mcp.json` na raiz do projeto.

```
meu-projeto/
└── .vscode/
    └── mcp.json
```

**Escopo global**: pressione `Ctrl+Shift+P` e execute `MCP: Open User Configuration`.

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub Personal Access Token",
      "password": true
    },
    {
      "type": "promptString",
      "id": "mysql-password",
      "description": "Senha do MySQL",
      "password": true
    },
    {
      "type": "promptString",
      "id": "sqlserver-password",
      "description": "Senha do SQL Server",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "mysql": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@benborla29/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "mcp_user",
        "MYSQL_PASS": "${input:mysql-password}",
        "MYSQL_DB": "nome_do_banco",
        "ALLOW_INSERT_OPERATION": "false",
        "ALLOW_UPDATE_OPERATION": "false",
        "ALLOW_DELETE_OPERATION": "false"
      }
    },
    "sqlserver": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bilims/mcp-sqlserver"],
      "env": {
        "SQLSERVER_HOST": "localhost",
        "SQLSERVER_PORT": "1433",
        "SQLSERVER_USER": "SEU_USUARIO",
        "SQLSERVER_PASSWORD": "${input:sqlserver-password}",
        "SQLSERVER_DATABASE": "nome_do_banco",
        "SQLSERVER_ENCRYPT": "false",
        "SQLSERVER_TRUST_CERT": "true"
      }
    },
    "rest-api": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "mcp-fetch-server"],
      "env": {
        "DEFAULT_LIMIT": "50000"
      }
    }
  }
}
```

> **`${input:variavel}`** é um recurso exclusivo do VS Code. Em vez de salvar senhas no arquivo, o VS Code pede o valor na primeira execução e o armazena de forma segura. Use sempre que possível.

### Como verificar se está funcionando

1. Pressione `Ctrl+Shift+P` e execute `MCP: List Servers`
2. Os quatro servidores devem aparecer com status `Connected`
3. Abra o Copilot Chat, mude para **modo Agent** (ícone de agente no chat)
4. Clique em `Configure Tools` para ativar as ferramentas de cada servidor

### Como usar no chat

No modo Agent, escreva perguntas diretas:

```
Liste as tabelas do banco mysql.
Quais são os repositórios que tenho no GitHub?
Mostre o schema da tabela clientes no SQL Server.
Busque https://viacep.com.br/ws/01310100/json/ e mostre o resultado.
```

---

## Usando o servidor REST API

O servidor `rest-api` usa o pacote `mcp-fetch-server` e expõe ferramentas para fazer requisições HTTP a qualquer URL. Ele suporta os formatos HTML, JSON, texto puro e Markdown.

### Ferramentas disponíveis

| Ferramenta | O que faz |
|---|---|
| `fetch_json` | Faz GET e retorna a resposta como JSON |
| `fetch_html` | Retorna o HTML bruto da URL |
| `fetch_markdown` | Converte o conteúdo da página para Markdown |
| `fetch_txt` | Retorna texto puro sem tags HTML |

### Exemplos com APIs públicas (sem autenticação)

Essas APIs são gratuitas e não exigem cadastro — ideais para começar.

**ViaCEP** — consulta de endereços por CEP (Brasil):

```
Busque o endereço do CEP 01310-100 usando a API do ViaCEP.
```

A IA fará uma requisição a `https://viacep.com.br/ws/01310100/json/` e retornará logradouro, bairro, cidade e UF.

**JSONPlaceholder** — API de testes com dados fictícios:

```
Use a API JSONPlaceholder para buscar os posts do usuário de id 1.
```

URL resultante: `https://jsonplaceholder.typicode.com/users/1/posts`

**Open-Meteo** — previsão do tempo sem API key:

```
Qual a temperatura atual em São Paulo? Use a API Open-Meteo com lat=-23.55 e lon=-46.63.
```

URL: `https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&current_weather=true`

### Exemplo com API autenticada (Bearer Token)

Para APIs que exigem autenticação via header, instrua a IA a incluir o token diretamente na requisição:

```
Busque https://api.exemplo.com/dados usando o header Authorization: Bearer MEU_TOKEN_AQUI
```

O `mcp-fetch-server` passa os headers que você especificar no prompt para a requisição HTTP.

> **Segurança:** nunca inclua tokens reais em histórico de chat. Para APIs internas com credenciais sensíveis, prefira criar um servidor MCP dedicado para aquela API específica.

---

## Criando o usuário de banco com permissões mínimas

Nunca use `root` ou `sa` nas configurações MCP. Crie usuários dedicados com acesso restrito.

### MySQL

Execute no MySQL como administrador:

```sql
-- Cria o usuário
CREATE USER 'mcp_user'@'localhost' IDENTIFIED BY 'senha_segura_aqui';

-- Concede apenas leitura no banco específico
GRANT SELECT ON nome_do_banco.* TO 'mcp_user'@'localhost';

-- Aplica as permissões
FLUSH PRIVILEGES;
```

### SQL Server

Execute no SQL Server Management Studio (SSMS) como administrador:

```sql
-- Cria o login no servidor
CREATE LOGIN mcp_user WITH PASSWORD = 'Senha@Segura123';

-- Cria o usuário no banco específico
USE nome_do_banco;
CREATE USER mcp_user FOR LOGIN mcp_user;

-- Concede apenas leitura
ALTER ROLE db_datareader ADD MEMBER mcp_user;
```

---

## Diagnóstico de problemas comuns

| Problema | Causa provável | Solução |
|---|---|---|
| Servidor não aparece na lista | Chave raiz errada | Verifique: `mcpServers` (Cursor/Claude Code) ou `servers` (VS Code) |
| Servidor trava ao iniciar | Falta do `cmd /c` no Windows | Adicione `"command": "cmd"` e `"args": ["/c", "npx", ...]` |
| Ferramentas não aparecem no VS Code | Modo errado | Mude para **modo Agent** no Copilot Chat |
| Erro de autenticação no GitHub | Token expirado ou escopo errado | Gere um novo PAT com `repo`, `read:org`, `read:user` |
| Conexão recusada no banco | Banco não está rodando | Execute `netstat -an \| findstr 3306` (MySQL) ou `1433` (SQL Server) |
| JSON inválido | Erro de sintaxe | Valide em [jsonlint.com](https://jsonlint.com) |

---

## Resumo: onde colocar cada arquivo

```
Windows — Caminhos de configuração
─────────────────────────────────────────────────────────────────
Claude Code
  Projeto:  <pasta-do-projeto>\.mcp.json
  Global:   C:\Users\SEU_USUARIO\.mcp.json

Cursor
  Projeto:  <pasta-do-projeto>\.cursor\mcp.json
  Global:   C:\Users\SEU_USUARIO\.cursor\mcp.json

VS Code
  Projeto:  <pasta-do-projeto>\.vscode\mcp.json
  Global:   via Ctrl+Shift+P → "MCP: Open User Configuration"
─────────────────────────────────────────────────────────────────
```

---

## Referências

- Documentação Claude Code MCP: [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/mcp)
- Documentação Cursor MCP: [cursor.com/docs/context/mcp](https://cursor.com/docs/context/mcp)
- Documentação VS Code MCP: [code.visualstudio.com/docs/copilot/customization/mcp-servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- Pacote MySQL MCP: [github.com/benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql)
- Pacote SQL Server MCP: [github.com/bilims/mcp-sqlserver](https://github.com/bilims/mcp-sqlserver)
- Pacote REST API MCP: [github.com/zcaceres/fetch-mcp](https://github.com/zcaceres/fetch-mcp)
- API de teste JSONPlaceholder: [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)
- API de CEP ViaCEP: [viacep.com.br](https://viacep.com.br)
- API de clima Open-Meteo: [open-meteo.com](https://open-meteo.com)
