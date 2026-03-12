# Documento de Visão do Produto

## 1. Identificação do Produto
Nome do produto: SolarCalc - Simulador de Viabilidade Fotovoltaica

Versão do documento: 1.0

Data: 12/03/2026

Equipe responsável: Equipe do projeto

## 2. Visão Geral
O SolarCalc é um simulador web voltado ao cálculo de viabilidade e tempo real de retorno (Payback) para investimentos em energia solar fotovoltaica.

O sistema busca trazer transparência e precisão para o consumidor, considerando fatores reais de localização e tarifas, e oferecendo uma projeção financeira clara do investimento.

## 3. Problema
Muitos proprietários investem em energia solar sem entender o tempo real de retorno do investimento (Payback). As decisões muitas vezes baseiam-se em estimativas vagas que ignoram fatores críticos, como sombreamento local, taxas específicas da concessionária de energia e a degradação dos painéis ao longo do tempo.

Isso gera incerteza financeira, expectativas frustradas e dificuldade na tomada de decisão sobre a instalação do sistema.

## 4. Objetivo do Produto
O produto tem como objetivo:

- calcular a viabilidade financeira e o tempo de retorno (Payback) de sistemas fotovoltaicos

- estimar a geração mensal de energia com base em dados climáticos e geográficos

- comparar os custos acumulados com a concessionária versus o custo do sistema solar

- prover dados precisos integrando índices de irradiação solar e tarifas de concessionárias

## 5. Público-Alvo
O sistema é destinado principalmente a:

- proprietários residenciais

- pequenos comerciantes

## 6. Principais Necessidades dos Usuários
### Proprietários Residenciais
- reduzir o valor da conta de luz (economia doméstica)

- valorizar o seu imóvel

- entender de forma simples em quanto tempo o sistema se paga

### Pequenos Comerciantes
- reduzir o custo operacional do negócio (OPEX)

- obter previsibilidade de caixa a longo prazo

- comparar de forma clara os cenários com e sem energia solar

## 7. Proposta de Valor
O sistema oferece uma simulação financeira e técnica precisa, baseada em dados reais e atualizados, permitindo que o usuário visualize com clareza o retorno do seu investimento.

Em vez de depender de orçamentos enviesados de vendedores, o produto fornece autonomia, transparência e segurança na decisão de investir em energia solar.

## 8. Funcionalidades Principais
- coleta de dados de consumo (média em kWh ou valor em Reais)

- identificação de localização (CEP ou cidade) e busca de índices de irradiação (HSP)

- especificação de área disponível (m²) e orientação do telhado

- seleção de perfil de conexão (Monofásica, Bifásica ou Trifásica)

- cálculo de geração estimada de energia

- cálculo e estimativa de Payback (em anos e meses)

- dashboard de gráfico comparativo de custos (concessionária vs. fotovoltaico)

## 9. Benefícios Esperados
- maior segurança na decisão de investimento

- transparência sobre os custos reais e o tempo de retorno

- agilidade na obtenção de uma análise de viabilidade confiável

- facilidade de compreensão dos dados financeiros e técnicos

## 10. Restrições e Premissas
### Restrições
- o sistema será uma aplicação web responsiva

- o fluxo de preenchimento deve ter no máximo 5 etapas

- o cálculo de projeção de 25 anos deve ocorrer em até 30 segundos

- o design dos gráficos deve ser acessível para daltônicos e ter legendas claras

- uso exclusivo do padrão monetário brasileiro (BRL) e sistema métrico decimal

### Premissas
 - o usuário tem acesso aos dados de sua conta de luz (consumo ou valor pago)

- haverá acesso à internet para integração com APIs de irradiação (SWERA/INPE)

- os dados de tarifas precisam ser atualizados mensalmente conforme resoluções da ANEEL

## 11. Diferenciais do Produto
- integração direta com APIs de índices de irradiação confiáveis (SWERA/INPE)

- suporte nativo às diferentes tarifas das concessionárias brasileiras

- cálculo que considera a taxa de disponibilidade por tipo de conexão (mono/bi/trifásica)

- foco absoluto na experiência do usuário, com acessibilidade e rapidez

## 12. Critérios de Sucesso
O produto será considerado bem-sucedido se:

- os usuários conseguirem concluir a simulação sem abandonar o fluxo (máximo de 5 etapas)

- os resultados forem gerados de forma rápida (abaixo de 30 segundos)

- as estimativas geradas refletirem com precisão as tarifas atualizadas da ANEEL

## 13. Escopo Inicial
O escopo inicial do produto inclui:

- cálculo de viabilidade e ROI

- integração com APIs de índices de irradiação (SWERA/INPE)

- suporte às tarifas das concessionárias brasileiras

- estimativa de payback

- dashboard comparativo responsivo

## 14. Fora do Escopo Inicial
Nesta primeira versão, não fazem parte do escopo:

- venda direta de equipamentos fotovoltaicos

- elaboração de projeto de engenharia para submissão à concessionária

- monitoramento em tempo real do sistema pós-instalação

## 15. Resumo Executivo
O SolarCalc é um simulador web que traz transparência para o mercado de energia fotovoltaica. Ao cruzar dados de consumo, localização e tarifas reais, o sistema permite que proprietários e comerciantes calculem a viabilidade e o tempo de retorno de seus investimentos de forma rápida, acessível e segura, eliminando a incerteza antes da compra de equipamentos.
