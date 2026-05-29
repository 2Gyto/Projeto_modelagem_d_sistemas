# Cálculo da quantidade de placas

Implementação em
[`app/application/calculadora_solar.py`](../src/backend/app/application/calculadora_solar.py).

A função é pura — recebe o **gasto mensal em R$** e devolve nº de placas,
potência do sistema, geração mensal estimada e economia mensal.

> **Aviso:** o MVP usa **médias brasileiras** como aproximação. As próximas
> iterações vão substituir as constantes por chamadas reais a Brasil API (CEP
> → coordenadas), NASA POWER (HSP da região) e Gemini (cotação dinâmica de
> equipamentos). A estrutura da função foi pensada para receber esses valores
> como parâmetros sem mudar a fórmula.

---

## Constantes (parâmetros padrão)

| Símbolo                | Valor          | Significado                                          |
| ---------------------- | -------------- | ---------------------------------------------------- |
| `TARIFA_PADRAO_REAIS_KWH` | `0,85`        | Tarifa média BR (R$/kWh)                             |
| `HSP_PADRAO_HORAS_DIA` | `5,0`          | Horas de Sol Pleno médias por dia (Brasil)           |
| `POTENCIA_PAINEL_KWP`  | `0,55`         | Potência de um painel comum hoje (550 Wp)            |
| `EFICIENCIA_SISTEMA`   | `0,80`         | Eficiência efetiva (perdas + inversor)               |
| `DIAS_MES`             | `30`           | Aproximação mensal                                   |

---

## Fórmula

### 1. Consumo mensal estimado (kWh)

A entrada é o gasto em R$. Convertemos por tarifa:

```
consumo_kwh_mes = valor_reais_mes ÷ tarifa_kwh
```

### 2. Geração por painel (kWh/mês)

```
geracao_por_painel = POTENCIA_PAINEL_KWP × HSP × DIAS_MES × EFICIENCIA_SISTEMA
                   = 0,55  × 5  × 30  × 0,80
                   = 66 kWh/mês  (com os defaults)
```

### 3. Quantidade de placas

```
quantidade_paineis = ⌈ consumo_kwh_mes ÷ geracao_por_painel ⌉
```

Arredondamos **para cima** porque não faz sentido instalar fração de painel,
e garantimos no mínimo 1 painel.

### 4. Métricas derivadas

```
geracao_total_kwh_mes  = geracao_por_painel × quantidade_paineis
potencia_sistema_kwp   = POTENCIA_PAINEL_KWP × quantidade_paineis
economia_mensal_reais  = min(consumo_kwh_mes, geracao_total_kwh_mes) × tarifa_kwh
```

A economia é limitada pelo consumo: gerar mais do que o consumido não
"economiza" mais (compensação futura na conta varia por concessionária e
foge do escopo do MVP).

---

## Exemplo numérico

Entrada: `valor_reais = 350`.

1. `consumo_kwh = 350 / 0,85  ≈ 411,76 kWh/mês`
2. `geracao_por_painel = 0,55 × 5 × 30 × 0,80 = 66 kWh/mês`
3. `quantidade_paineis = ⌈411,76 / 66⌉ = ⌈6,239⌉ = 7 placas`
4. `geracao_total = 66 × 7 = 462 kWh/mês`
5. `potencia_sistema = 0,55 × 7 = 3,85 kWp`
6. `economia = min(411,76, 462) × 0,85 = 411,76 × 0,85 ≈ R$ 350,00 /mês`

Esse é exatamente o resultado que o backend retorna para o caso `R$ 350`:

```json
{
  "consumo_kwh_mes": "411.76",
  "quantidade_paineis": 7,
  "potencia_sistema_kwp": "3.85",
  "geracao_total_kwh_mes": "462.00",
  "economia_mensal_reais": "350.00"
}
```

---

## Próximos passos da calculadora

1. **Tarifa real por concessionária** — usar `tarifas_concessionarias` (já
   existe no schema) em vez do default `0,85`. Lookup pelo CEP/cidade.
2. **HSP real** — chamar NASA POWER (`infrastructure/external/nasa_power.py`)
   com as coordenadas do CEP convertidas via Brasil API.
3. **Potência de painel dinâmica** — `Gemini` para descobrir o painel mais
   comum no varejo BR no momento.
4. **Payback** — com custo total estimado e economia mensal, calcular
   `payback_meses` e `payback_anos` (os campos já existem em `resultados`).
5. **Projeção de 25 anos** — gerar registros em `projecoes_anuais` com
   degradação anual de geração (~0,5–0,7%/ano) e inflação tarifária
   (configurável).

A fórmula já recebe `tarifa_kwh` e `hsp` como parâmetros opcionais, então
substituir os defaults por valores reais é uma troca de uma linha no service.
