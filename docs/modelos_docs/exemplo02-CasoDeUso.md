# Caso de Uso 002

**Nome:** Cadastrar produto  
**Atores:** Administrador, Sistema de Estoque  
**Objetivo:** Permitir o cadastro de um novo produto no sistema.  

## Descrição

Este caso de uso descreve o processo de inclusão de um novo produto no sistema de estoque.

## Pré-condições

- o administrador deve estar autenticado no sistema
- o administrador deve ter permissão de cadastro

## Fluxo principal

1. O administrador acessa a tela de cadastro de produtos.
2. O sistema exibe o formulário de cadastro.
3. O administrador informa os dados do produto.
4. O administrador confirma o cadastro.
5. O sistema valida os dados informados.
6. O sistema registra o novo produto.
7. O sistema exibe a mensagem de sucesso.

## Fluxos alternativos

### A1. Dados obrigatórios não preenchidos

1. No passo 5, o sistema identifica campos obrigatórios em branco.
2. O sistema informa os campos que devem ser corrigidos.
3. O administrador ajusta os dados e reenvi a solicitação.

### A2. Produto já cadastrado

1. No passo 5, o sistema verifica que já existe um produto com o mesmo código.
2. O sistema informa que o cadastro não pode ser concluído.

## Pós-condições

- o produto fica registrado no sistema
- o produto passa a estar disponível para consulta e movimentação no estoque