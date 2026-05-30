# ADR 002

**Título:** Adoção de microsserviços no sistema de e-commerce  
**Data:** 13/08/2023  
**Responsável:** Maria Santos  
**Status:** Aceito  

## Contexto

Durante a definição da arquitetura do novo sistema de e-commerce, a equipe precisou escolher como organizar a aplicação. O sistema envolve catálogo de produtos, pedidos, pagamentos e interação com usuários, o que exige uma solução que suporte crescimento e evolução do projeto.

## Decisão

Foi adotada uma arquitetura baseada em **microsserviços**.

## Justificativa

A escolha foi feita pelos seguintes motivos:

- permite escalar partes específicas do sistema conforme a demanda
- facilita o trabalho de equipes em funcionalidades diferentes
- torna manutenção e atualização mais isoladas
- oferece mais flexibilidade na escolha de tecnologias
- reduz o impacto de falhas em componentes específicos

## Alternativas consideradas

### Monolito

Foi considerado por ser mais simples no início. Mesmo assim, foi descartado porque poderia dificultar a evolução, a manutenção e a escalabilidade do sistema.

### Arquitetura em camadas

Também foi avaliada. Apesar de organizar bem a aplicação, foi considerada menos adequada para evolução independente dos módulos do sistema.

## Consequências

Com essa decisão, o sistema passa a ter:

- maior flexibilidade para crescimento
- equipes com mais autonomia no desenvolvimento
- melhor isolamento entre funcionalidades

Como pontos de atenção, a equipe precisará lidar com:

- maior complexidade na gestão dos serviços
- definição de padrões de comunicação entre os microsserviços
- esforço inicial maior na configuração da arquitetura