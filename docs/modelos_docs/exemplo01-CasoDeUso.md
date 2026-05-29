# Caso de Uso 001

**Nome:** Realizar matrícula  
**Atores:** Aluno, Sistema Acadêmico  
**Objetivo:** Permitir que o aluno se matricule em uma disciplina.  

## Descrição

Este caso de uso descreve o processo em que o aluno seleciona uma disciplina e solicita sua matrícula no sistema.

## Pré-condições

- o aluno deve estar autenticado no sistema
- a disciplina deve estar disponível para matrícula
- o período de matrícula deve estar aberto

## Fluxo principal

1. O aluno acessa a área de matrícula.
2. O sistema exibe as disciplinas disponíveis.
3. O aluno seleciona a disciplina desejada.
4. O sistema verifica se há vagas.
5. O sistema verifica se o aluno atende aos pré-requisitos.
6. O aluno confirma a solicitação.
7. O sistema registra a matrícula.
8. O sistema exibe a confirmação da operação.

## Fluxos alternativos

### A1. Disciplina sem vagas

1. No passo 4, o sistema identifica que não há vagas disponíveis.
2. O sistema informa que a matrícula não pode ser realizada.

### A2. Pré-requisito não atendido

1. No passo 5, o sistema identifica que o aluno não atende aos pré-requisitos.
2. O sistema informa que a matrícula não pode ser concluída.

## Pós-condições

- a matrícula é registrada no sistema
- a vaga da disciplina é atualizada
- o aluno passa a visualizar a disciplina em sua grade