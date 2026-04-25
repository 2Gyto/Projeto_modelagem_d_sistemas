# Requisitos Funcionais do Sistema Fotovoltaico

## RF01 – Coleta de Consumo
O sistema deve permitir que o usuário insira:
- A média de consumo mensal de energia em **kWh**, ou
- O valor médio da conta de energia em **Reais (R$)**.

Esses dados serão utilizados como base para os cálculos de dimensionamento do sistema fotovoltaico.

<a id="rf-01-1"></a>
### RF01.1 – Equivalência em kWh a partir do valor em reais (R$)

Quando o usuário informar apenas o **valor médio da conta em R$**, o sistema deve calcular o **consumo mensal equivalente em kWh** antes de prosseguir com o dimensionamento.

**Regra de cálculo:**  
`consumo_kwh_mes = valor_medio_conta_reais / tarifa_kwh_aplicada`

Onde `tarifa_kwh_aplicada` é o **preço de referência por kWh (R$/kWh)** utilizado nos cálculos da mesma simulação para comparar o custo com a concessionária (o mesmo registro tarifário vigente aplicado à projeção da fatura “sem solar”), de modo a manter **consistência** entre a conversão R$→kWh e a projeção financeira.

**Transparência:** o sistema deve exibir de forma legível o valor de **kWh/mês** obtido a partir do valor em R$ informado (por exemplo, na etapa de revisão ou no resumo dos resultados).

---

## RF02 – Localização Geográfica
O sistema deve permitir que o usuário informe:
- O **CEP**, ou
- A **cidade**.

A partir dessas informações, o sistema deve buscar automaticamente os **índices de irradiação solar da região**, utilizando o índice **HSP (Hours of Full Sun)**.

---

## RF03 – Especificação de Área
O sistema deve permitir que o usuário informe:
- A **área disponível para instalação** dos painéis solares (em m²).
- A **orientação do telhado**, podendo selecionar entre:
  - Norte
  - Sul
  - Leste
  - Oeste

Essas informações serão utilizadas para estimar a capacidade máxima de instalação do sistema.

---

## RF04 – Seleção de Perfil de Conexão
O sistema deve permitir que o usuário selecione o tipo de conexão elétrica da residência ou estabelecimento:

- Monofásica
- Bifásica
- Trifásica

Com base nessa escolha, o sistema deverá considerar a **taxa de disponibilidade da concessionária** no cálculo do consumo mínimo faturado.

---

## RF05 – Cálculo de Geração Estimada
O sistema deve calcular a **produção mensal estimada de energia** considerando:

- Potência do sistema fotovoltaico selecionado
- Índice de irradiação solar da região (HSP)
- Eficiência média do sistema

O resultado deve ser apresentado em **kWh/mês**.

---

## RF06 – Estimativa de Payback
O sistema deve calcular o **tempo estimado de retorno do investimento (payback)** com base em:

- Custo estimado do sistema fotovoltaico
- Economia mensal na conta de energia
- Tarifas energéticas médias

O resultado deve ser apresentado em:
- **Anos**
- **Meses**

---

## RF07 – Dashboard Comparativo
O sistema deve apresentar um **dashboard visual comparativo**, contendo:

- Um **gráfico de custo acumulado ao longo do tempo**
- Comparação entre:
  - **Custo acumulado com a concessionária**
  - **Custo com investimento no sistema fotovoltaico**

O gráfico deve permitir visualizar o ponto em que ocorre o **payback do sistema**.

---

# Observações
- Todos os cálculos devem considerar valores médios de mercado e parâmetros configuráveis.
- O sistema deve apresentar os resultados de forma clara e visual para facilitar a tomada de decisão do usuário.
