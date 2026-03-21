# Caso de Uso Nº 01

**Nome:** Realizar login no sistema  
**Atores:** Usuário, Sistema SolarCalc  
**Objetivo:** Permitir que o usuário acesse sua conta no sistema para utilizar as funcionalidades do simulador.  

## Descrição

ste caso de uso descreve o processo em que o usuário informa suas credenciais de acesso para autenticar-se no sistema e acessar as funcionalidades disponíveis.

## Pré-condições

- o usuário deve possuir uma conta cadastrada no sistema

- sistema SolarCalc deve estar disponível


## Fluxo principal

Descreva a sequência principal de passos do caso de uso.

1. O usuário acessa a página de login do sistema.
2. O sistema exibe o formulário de autenticação.
3. O usuário informa seu e-mail e senha.  
4. O usuário confirma a solicitação de login.  
5. O sistema valida as credenciais informadas. 
6. O sistema autentica o usuário.
7. O sistema redireciona o usuário para a página principal do simulador.
## Fluxos alternativos

Descreva situações em que o fluxo principal não segue o caminho esperado.

### A1. Credenciais inválidas

1. No passo 5, o sistema identifica que o e-mail ou senha estão incorretos. 
2. O sistema informa que as credenciais são inválidas. 
3. O usuário pode tentar realizar o login novamente.  

### A2. Campos obrigatórios não preenchidos

1. No passo 5, o sistema identifica que algum campo está em branco.  
2. O sistema informa quais campos precisam ser preenchidos.
3. O usuário corrige os dados e tenta novamente.

### A2. Campos obrigatórios não preenchidos
1. No passo 5, o sistema verifica que o e-mail informado não possui cadastro.
2. O sistema informa que o usuário não está registrado.
3. O sistema sugere que o usuário realize o cadastro.
## Pós-condições

- o usuário é autenticado no sistema
- o usuário passa a ter acesso às funcionalidades do simulador

