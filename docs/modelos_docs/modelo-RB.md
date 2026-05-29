# Modelo de Regras de Negócio

## Instruções

Regras de negócio descrevem normas, restrições, condições e critérios que o sistema deve respeitar.

Elas ajudam a definir como o domínio funciona na prática.

Escreva as regras de forma clara, objetiva e direta.

---

## Exemplo de escrita

- O aluno só pode se matricular em disciplinas com vagas disponíveis.
- O cliente só pode cancelar um pedido antes da emissão da nota fiscal.
- Somente administradores podem excluir usuários do sistema.

---

## Modelo para preenchimento

### RB01. __________________________
____________________________________________________________  
____________________________________________________________  

### RB02. __________________________
____________________________________________________________  
____________________________________________________________  

### RB03. __________________________
____________________________________________________________  
____________________________________________________________  

### RB04. __________________________
____________________________________________________________  
____________________________________________________________  

### RB05. __________________________
____________________________________________________________  
____________________________________________________________  

---

## Estrutura recomendada

Uma boa forma de escrever é:

**Entidade ou ator + condição/regra + consequência**

**Exemplos:**

- O aluno só pode realizar matrícula se estiver com status ativo.
- O sistema deve bloquear a venda de produtos sem estoque disponível.
- O professor só pode lançar notas das turmas em que está vinculado.

---

## Tipos comuns de regras de negócio

### Limites
Definem quantidades máximas, mínimas ou faixas permitidas.

**Exemplos:**
- o cliente pode comprar no máximo 5 unidades por item
- o aluno pode cursar no máximo 8 disciplinas por semestre

### Condições
Definem o que precisa ser verdadeiro para uma ação ocorrer.

**Exemplos:**
- a matrícula só pode ocorrer no período definido
- o pedido só pode ser cancelado antes do pagamento ser confirmado

### Restrições de acesso
Definem quem pode executar determinadas ações.

**Exemplos:**
- somente administradores podem excluir cadastros
- apenas professores da disciplina podem lançar notas

### Critérios de cálculo ou validação
Definem regras para aprovar, calcular ou validar dados.

**Exemplos:**
- a aprovação exige nota mínima 6,0
- o desconto é aplicado apenas em compras acima de determinado valor

---

## Orientações para os alunos

- escreva regras que representem normas reais do domínio
- evite descrever telas ou botões
- evite confundir regra de negócio com requisito funcional
- pense em restrições, validações e condições que o sistema precisa obedecer
- use frases objetivas e verificáveis