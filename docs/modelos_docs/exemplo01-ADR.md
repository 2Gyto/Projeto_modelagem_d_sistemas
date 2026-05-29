```md
# ADR 001

**Título:** Escolha do banco de dados  
**Data:** 13/08/2023  
**Responsável:** Equipe do projeto  
**Status:** Aceito  

## Contexto

No início do desenvolvimento do sistema de inventário, foi necessário definir qual banco de dados seria usado. A escolha precisava considerar a organização dos dados, a confiabilidade das operações e a manutenção futura do sistema.

## Decisão

Foi escolhido o PostgreSQL como banco de dados da aplicação.

## Justificativa

A escolha foi feita pelos seguintes motivos:

- o sistema possui dados relacionados entre si, como produtos, fornecedores, pedidos e estoque
- é importante garantir consistência nas operações
- o PostgreSQL oferece suporte a transações e integridade dos dados
- é uma tecnologia estável, bem documentada e amplamente usada

## Alternativas consideradas

### MongoDB

Foi analisado, mas não foi priorizado porque o sistema exige relações bem definidas entre os dados e maior controle de consistência.

### MySQL

Também foi avaliado. Apesar de ser uma solução relacional conhecida, o PostgreSQL foi considerado mais adequado para as necessidades do projeto.

## Consequências

Com essa decisão, o sistema passa a ter:

- uma base relacional adequada ao domínio do problema
- mais segurança nas operações de cadastro e movimentação
- maior facilidade para consultas com relacionamentos entre dados

Como ponto de atenção, a equipe precisa conhecer bem a modelagem relacional e os recursos do PostgreSQL.
```
