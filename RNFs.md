# Requisitos Não Funcionais
## RNF01. Desempenho e Integração
O sistema deve processar o cálculo de viabilidade de 25 anos e exibir o dashboard de resultados em, no máximo, 30 segundos.

Este limite de tempo inclui o processamento interno e as requisições externas em cadeia para a Brasil API, NASA POWER API e Gemini API.

## RNF02. Usabilidade e Retenção
O fluxo de simulação não deve exceder 5 etapas de preenchimento de dados para evitar o abandono do usuário.

Os gráficos do dashboard comparativo devem ser acessíveis, utilizando texturas ou paletas de cores com contraste adequado para daltônicos.

## RNF03. Portabilidade e Acessibilidade
O simulador deve ser uma aplicação web totalmente responsiva.

A interface deve adaptar-se adequadamente a resoluções de telas de smartphones, tablets e desktops nos navegadores mais modernos (Chrome, Firefox, Edge e Safari).

## RNF04. Confiabilidade e Padronização de Dados
O sistema deve apresentar todos os valores financeiros exclusivamente em Real brasileiro (BRL) e medidas físicas no sistema métrico decimal (m²).

O banco de dados de tarifas das concessionárias de energia deve permitir atualização mensal para refletir as resoluções vigentes da ANEEL.

## RNF05. Tolerância a Falhas (Tratamento de Exceções)
O sistema deve tratar a indisponibilidade das APIs externas (Brasil API, NASA, Gemini) sem causar o travamento da aplicação.

Caso o tempo limite de resposta (timeout) de 10 segundos de uma API seja atingido, o sistema deve exibir uma mensagem de erro clara ao usuário orientando a tentar novamente mais tarde.
