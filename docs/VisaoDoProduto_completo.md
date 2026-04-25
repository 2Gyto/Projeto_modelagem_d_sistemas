# Documento de Visão do Produto

**Nome do produto:** SolarCalc — Simulador de Viabilidade Fotovoltaica  
**Versão do documento:** 2.0  
**Data:** 24/04/2026  
**Status:** Revisado e Expandido

**Equipe responsável:**
- Arthur De Almeida Santos
- Gabriel Andre Iunis De Paula
- Gabriel Lopes Montalvao

**Histórico de Revisões:**

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 12/03/2026 | Equipe SolarCalc | Versão inicial |
| 1.1 | 20/03/2026 | Equipe SolarCalc | Ajustes gerais |
| 2.0 | 24/04/2026 | Equipe SolarCalc | Expansão completa do documento |

---

## 1. Identificação do Produto

O **SolarCalc** é um simulador web voltado ao cálculo de viabilidade e tempo real de retorno (Payback) para investimentos em energia solar fotovoltaica, destinado a proprietários residenciais e pequenos comerciantes brasileiros.

---

## 2. Visão Geral

O SolarCalc é um simulador web que traz transparência para o mercado de energia fotovoltaica. O sistema busca trazer precisão para o consumidor, considerando fatores reais de localização, tarifas e custos atualizados de equipamentos, oferecendo uma projeção financeira clara do investimento com o apoio de inteligência artificial.

Ao cruzar dados de consumo com coordenadas geográficas exatas (Brasil API), dados climáticos da agência espacial americana (NASA POWER API) e inteligência artificial para cotação de equipamentos (Gemini API), o sistema permite que proprietários e comerciantes calculem a viabilidade e o tempo de retorno de seus investimentos de forma rápida, acessível e segura, eliminando a incerteza antes da compra.

---

## 3. Problema

### 3.1 Descrição do Problema

Muitos proprietários investem em energia solar sem entender o tempo real de retorno do investimento (Payback). As decisões muitas vezes baseiam-se em estimativas vagas que ignoram fatores críticos, como o índice de irradiação exato do local, taxas específicas da concessionária e a variação constante de preços e marcas de equipamentos no mercado.

Isso gera **incerteza financeira**, **expectativas frustradas** e **dificuldade na tomada de decisão** sobre a instalação do sistema.

### 3.2 Impacto do Problema

| Afetado | Impacto |
|---------|---------|
| Proprietário residencial | Investimento realizado sem base real, gerando frustração e endividamento |
| Pequeno comerciante | Projeções incorretas de economia comprometem o planejamento financeiro do negócio |
| Mercado fotovoltaico | Falta de confiança do consumidor desacelera a adoção de energia limpa |

### 3.3 Causas Raiz

- Ausência de ferramentas gratuitas e precisas de simulação acessíveis ao público geral
- Dependência de orçamentos fornecidos por vendedores com interesse comercial direto
- Falta de integração entre dados climáticos, tarifários e de mercado em uma única ferramenta
- Complexidade técnica dos cálculos de irradiação e dimensionamento de sistemas fotovoltaicos

---

## 4. Objetivo do Produto

O produto tem como objetivo principal democratizar o acesso à análise de viabilidade de energia solar, oferecendo:

- **Cálculo de viabilidade financeira** e o tempo de retorno (Payback) de sistemas fotovoltaicos
- **Estimativa de geração mensal de energia** com base em coordenadas geográficas e dados climáticos da NASA
- **Comparação dos custos acumulados** com a concessionária versus o custo do sistema solar
- **Dados precisos de custos e marcas de painéis** utilizando inteligência artificial via Gemini API

### 4.1 Objetivos Mensuráveis

| Objetivo | Métrica de Sucesso |
|----------|--------------------|
| Fluxo simples | Simulação concluída em até 5 etapas |
| Desempenho | Cálculo de 25 anos em menos de 30 segundos |
| Precisão | Estimativas dentro de ±10% da realidade de mercado |
| Adoção | Usuários concluem a simulação sem abandonar o fluxo |

---

## 5. Público-Alvo

O sistema é destinado principalmente a:

### 5.1 Proprietários Residenciais
Pessoas físicas donas de imóveis que desejam avaliar a viabilidade de instalar painéis solares em suas residências, preocupadas com a redução da conta de luz e com a valorização do imóvel.

*Referência: Persona Carlos Almeida — ver [personas.md](personas.md)*

### 5.2 Pequenos Comerciantes
Gestores e administradores financeiros de pequenas empresas (restaurantes, padarias, mercados, etc.) que buscam reduzir custos operacionais de energia e precisam de dados concretos para justificar o investimento.

*Referência: Persona Mariana Torres — ver [personas.md](personas.md)*

---

## 6. Principais Necessidades dos Usuários

### 6.1 Proprietários Residenciais
- Reduzir o valor da conta de luz (economia doméstica)
- Valorizar o seu imóvel
- Entender de forma simples em quanto tempo o sistema se paga
- Ter uma noção realista dos preços dos painéis disponíveis no mercado

### 6.2 Pequenos Comerciantes
- Reduzir o custo operacional do negócio (OPEX)
- Obter previsibilidade de caixa a longo prazo
- Comparar de forma clara os cenários com e sem energia solar
- Gerar relatório para apresentação aos sócios

---

## 7. Proposta de Valor

O SolarCalc oferece uma simulação financeira e técnica precisa, baseada em dados espaciais globais e inteligência artificial, permitindo que o usuário visualize com clareza o retorno do seu investimento.

Em vez de depender de orçamentos enviesados de vendedores, o produto fornece:

- **Autonomia** — o usuário realiza a análise sem depender de terceiros
- **Transparência** — custos reais dos equipamentos obtidos via IA
- **Segurança** — dados climáticos validados pela NASA
- **Agilidade** — análise completa em menos de 30 segundos

---

## 8. Funcionalidades Principais

| ID | Funcionalidade | Descrição | Requisito |
|----|---------------|-----------|-----------|
| F01 | Coleta de Consumo | Entrada de consumo em kWh ou valor em R$ | [RF01](RF.md#rf01) |
| F02 | Localização Geográfica | Conversão de CEP em coordenadas via Brasil API | [RF02](RF.md#rf02) |
| F03 | Especificação de Área | Área disponível em m² e orientação do telhado | [RF03](RF.md#rf03) |
| F04 | Perfil de Conexão | Seleção entre Monofásica, Bifásica ou Trifásica | [RF04](RF.md#rf04) |
| F05 | Geração Estimada | Cálculo de produção mensal em kWh com dados NASA | [RF05](RF.md#rf05) |
| F06 | Payback | Estimativa de retorno do investimento em anos e meses | [RF06](RF.md#rf06) |
| F07 | Dashboard Comparativo | Gráfico de custo acumulado concessionária vs fotovoltaico | [RF07](RF.md#rf07) |

---

## 9. Benefícios Esperados

- **Maior segurança na decisão de investimento** — dados precisos eliminam a necessidade de confiar apenas em vendedores
- **Estimativas de geração altamente precisas** — dados validados pela NASA POWER API
- **Transparência sobre os custos reais dos equipamentos** — atualização via Gemini API
- **Agilidade na obtenção de análise de viabilidade** — resultado completo em menos de 30 segundos
- **Acessibilidade para diferentes perfis** — interface simples para usuários sem conhecimento técnico

---

## 10. Restrições e Premissas

### 10.1 Restrições

| Restrição | Descrição |
|-----------|-----------|
| Plataforma | Aplicação web responsiva (sem app mobile nativo) |
| Fluxo | Máximo de 5 etapas de preenchimento |
| Desempenho | Cálculo de projeção de 25 anos em até 30 segundos |
| Acessibilidade | Gráficos acessíveis para daltônicos com legendas claras |
| Moeda/Medidas | Exclusivamente BRL e sistema métrico decimal |
| Idioma | Português brasileiro |

### 10.2 Premissas

- O usuário tem acesso aos dados de sua conta de luz (consumo ou valor pago)
- As APIs de terceiros (Brasil API, NASA POWER e Gemini API) estarão disponíveis com tempo de resposta adequado
- Os dados de tarifas serão atualizados mensalmente conforme resoluções da ANEEL
- O usuário dispõe de navegador moderno com acesso à internet

---

## 11. Diferenciais do Produto

### 11.1 Geolocalização Inteligente
Uso da Brasil API para converter o CEP do usuário em coordenadas exatas de forma transparente, eliminando erros de localização que impactariam na precisão dos cálculos de irradiação.

### 11.2 Dados Climáticos de Alta Precisão
Integração com a NASA POWER API, garantindo índices de irradiação solar globais e validados cientificamente, com histórico de mais de 30 anos de dados meteorológicos.

### 11.3 Orçamento Dinâmico com IA
Utilização da Gemini API para buscar ativamente informações sobre marcas e preços de mercado dos painéis, evitando que o sistema fique com valores defasados.

### 11.4 Cálculo de Taxa de Disponibilidade
Considera a taxa mínima de disponibilidade por tipo de conexão elétrica (monofásica, bifásica ou trifásica), alinhado às normas da ANEEL.

### 11.5 Acessibilidade Visual
Dashboard com paletas de cores com contraste adequado para daltônicos e legendas claras, conforme diretrizes de acessibilidade web.

---

## 12. Critérios de Sucesso

O produto será considerado bem-sucedido se:

| Critério | Meta |
|---------|------|
| Conclusão do fluxo | Usuários concluem a simulação sem abandonar (máximo de 5 etapas) |
| Integração fluida | Comunicação entre as 3 APIs abaixo de 30 segundos |
| Precisão | Estimativas refletem com precisão a realidade de mercado e tarifas da ANEEL |
| Acessibilidade | Interface utilizável em smartphones, tablets e desktops |

---

## 13. Arquitetura e Integrações

### 13.1 Visão Geral da Arquitetura

O SolarCalc adota uma **arquitetura monolítica organizada em camadas**, conforme decisão registrada no [ADR Nº 02](ADRs.md#adr-02).

As camadas são:
- **Interface (Frontend)** — formulário em múltiplas etapas e dashboard de resultados
- **Lógica de Aplicação** — cálculos de geração, payback e dimensionamento
- **Integração com APIs** — orquestração das chamadas externas
- **Acesso a Dados** — tarifas ANEEL e histórico de simulações

### 13.2 APIs Externas Integradas

| API | Finalidade | ADR |
|-----|-----------|-----|
| Brasil API | Conversão de CEP em coordenadas geográficas | [ADR Nº 05](ADRs.md#adr-05) |
| NASA POWER API | Índices de irradiação solar (HSP) por localização | [ADR Nº 05](ADRs.md#adr-05) |
| Gemini API | Preços e marcas de painéis solares atualizados | [ADR Nº 05](ADRs.md#adr-05) |

### 13.3 Estratégia de Tolerância a Falhas
Conforme [ADR Nº 03](ADRs.md#adr-03) e [RNF05](RNFs.md#rnf05), cada API possui timeout de 10 segundos, com mensagens de erro claras exibidas ao usuário em caso de falha.

---

## 14. Requisitos Não Funcionais (Resumo)

| ID | Categoria | Requisito | Detalhes |
|----|----------|-----------|---------|
| RNF01 | Desempenho | Simulação completa em ≤ 30s | Inclui todas as chamadas de API |
| RNF02 | Usabilidade | Máximo 5 etapas de preenchimento | Gráficos acessíveis para daltônicos |
| RNF03 | Portabilidade | Web responsivo | Chrome, Firefox, Edge e Safari |
| RNF04 | Confiabilidade | Valores em BRL e sistema métrico | Tarifas atualizadas mensalmente |
| RNF05 | Tolerância a Falhas | Timeout de 10s por API | Mensagem de erro clara ao usuário |

*Referência completa: [RNFs.md](RNFs.md)*

---

## 15. Escopo Inicial

### 15.1 Dentro do Escopo (v1.0)

- Cálculo de viabilidade e ROI
- Fluxo de geolocalização (CEP → Coordenadas via Brasil API)
- Integração com a NASA POWER API para índices de irradiação
- Integração com a Gemini API para consulta de dados de equipamentos
- Suporte às tarifas das concessionárias brasileiras (ANEEL)
- Dashboard comparativo responsivo
- Autenticação de usuários e histórico de simulações

### 15.2 Fora do Escopo Inicial

- Venda direta de equipamentos fotovoltaicos
- Elaboração de projeto de engenharia para submissão à concessionária
- Monitoramento em tempo real do sistema pós-instalação
- Versão mobile nativa (iOS/Android)
- Integração com sistemas de financiamento bancário
- Suporte a moedas estrangeiras

---

## 16. Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Indisponibilidade de APIs externas | Média | Alto | Timeout de 10s + mensagem de erro (ADR Nº 03) |
| Dados de irradiação imprecisos | Baixa | Alto | Uso exclusivo da NASA POWER API (dado científico validado) |
| Tarifas ANEEL desatualizadas | Média | Médio | Alerta ao usuário + atualização mensal obrigatória (RB07) |
| Abandono do fluxo pelo usuário | Média | Médio | Máximo de 5 etapas + UX simplificada (RNF02) |
| Preços de painéis defasados | Baixa | Médio | Consulta dinâmica via Gemini API |

---

## 17. Revisão e Validação

### 17.1 Critérios de Revisão do Documento

Este documento deve ser revisado sempre que:
- Houver mudança de escopo aprovada pela equipe
- Novas decisões arquiteturais forem tomadas (ADRs)
- Os requisitos funcionais ou não funcionais forem alterados
- Houver feedback dos stakeholders que impacte a visão do produto

### 17.2 Responsáveis pela Validação

| Papel | Responsável |
|-------|------------|
| Revisão técnica | Gabriel Andre Iunis De Paula |
| Revisão de arquitetura | Gabriel Lopes Montalvao |
| Aprovação final | Arthur De Almeida Santos |

### 17.3 Data da Próxima Revisão Programada

Quinze dias após o início da fase de implementação, ou quando houver alteração relevante nos requisitos.

---

## 18. Glossário

| Termo | Definição |
|-------|-----------|
| HSP | Hours of Sun Peak — Horas de pico de sol, índice de irradiação solar |
| Payback | Tempo necessário para recuperar o investimento inicial com as economias geradas |
| ANEEL | Agência Nacional de Energia Elétrica — órgão regulador do setor elétrico brasileiro |
| kWh | Quilowatt-hora — unidade de medida de energia elétrica |
| BRL | Real Brasileiro — moeda oficial do Brasil |
| CEP | Código de Endereçamento Postal — código postal brasileiro |
| OPEX | Operational Expenditure — custos operacionais recorrentes |
| ROI | Return on Investment — retorno sobre o investimento |
| API | Application Programming Interface — interface de programação de aplicações |
| Monofásica | Tipo de ligação elétrica residencial com uma fase e um neutro |
| Bifásica | Tipo de ligação elétrica com duas fases |
| Trifásica | Tipo de ligação elétrica comercial/industrial com três fases |

---

## 19. Referências Documentais

| Documento | Descrição | Localização |
|-----------|-----------|------------|
| RF.md | Requisitos Funcionais do Sistema | [RF.md](RF.md) |
| RNFs.md | Requisitos Não Funcionais | [RNFs.md](RNFs.md) |
| RB.md | Regras de Negócio | [RB.md](RB.md) |
| personas.md | Personas dos Usuários | [personas.md](personas.md) |
| ADRs.md | Decisões de Arquitetura | [ADRs.md](ADRs.md) |
| ModeloDominio.md | Modelo de Domínio | [ModeloDominio.md](ModeloDominio.md) |
