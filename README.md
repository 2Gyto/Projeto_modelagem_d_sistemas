# ☀️ SolarCalc - Simulador de Viabilidade Fotovoltaica

## Visão do Produto
Problema: Proprietários investem em energia solar sem entender o tempo real de retorno (Payback), baseando-se em estimativas vagas que não consideram sombreamento local, taxas da concessionária ou degradação dos painéis.

2. Público-Alvo
Proprietários Residenciais: Focados em economia doméstica e valorização do imóvel.

Pequenos Comerciantes: Focados em redução de custo operacional (OPEX) e previsibilidade de caixa.

3. Escopo e Fora de Escopo
No Escopo: Cálculo de viabilidade, Integração com APIs de índices de irradiação (SWERA/INPE), cálculo de ROI, suporte a diferentes tarifas de concessionárias brasileiras.

Fora de Escopo:  O sistema não fará a venda direta de equipamentos, não fará o projeto de engenharia para submissão à concessionária e não fará o monitoramento em tempo real pós-instalação.

4. Requisitos funcionais (RF)
RF01 – Coleta de Consumo: O sistema deve permitir que o usuário insira a média de consumo mensal de energia em kWh ou o valor médio da conta em Reais.

RF02 – Localização Geográfica: O sistema deve permitir que o usuário informe o CEP ou selecione a cidade para buscar os índices de irradiação solar (índice HSP - Hours Full Sun).

RF03 – Especificação de Área: O sistema deve permitir a entrada da área disponível para instalação (m²) e a orientação do telhado (Norte, Sul, Leste, Oeste).

RF04 – Seleção de Perfil: O sistema deve permitir que o usuário selecione o tipo de conexão (Monofásica, Bifásica ou Trifásica) para calcular a taxa de disponibilidade.

RF05 – Cálculo de Geração Estimada: O sistema deve calcular a produção mensal de energia com base na potência do sistema escolhido e nos dados climáticos da região.

RF06 – Estimativa de Payback: O sistema deve calcular o tempo de retorno do investimento (em anos e meses).

RF07 – Dashboard Comparativo: O sistema deve exibir um gráfico comparativo entre o custo acumulado com a concessionária vs. o custo com o sistema fotovoltaico ao longo do tempo.

5. Requisitos Não Funcionais (RNF)
RNF01 -Desempenho: O cálculo de projeção de 25 anos deve ser processado em até 30 segundos.

RNF02 - Portabilidade: O dashboard deve ser responsivo (acessível via web)

RNF03 - Confiabilidade: Os dados de tarifas devem ser atualizados mensalmente conforme resoluções da ENEEL.

RNF04 - Design Intuitivo: O fluxo de preenchimento (do CEP ao resultado) não deve exceder 5 etapas para evitar o abandono do usuário.

RNF05 - Visualização de Dados: Os gráficos do Dashboard Comparativo (RF07) devem possuir legendas claras e suporte a daltônicos (uso de texturas ou paletas de cores acessíveis).

RNF06 - Localização: O sistema deve utilizar o padrão monetário brasileiro (BRL) e o sistema métrico decimal para áreas e distâncias.
