# Regras de Negócio — SolarCalc

## RB01. Validação de consumo
O usuário deve informar um valor de consumo mensal válido (em kWh ou em reais) maior que zero.  
Caso contrário, o sistema deve impedir a simulação.

---

## RB02. Conversão de localização
O sistema só pode realizar a simulação após converter o CEP em coordenadas geográficas válidas.  
Caso o CEP seja inválido ou não encontrado, a simulação deve ser bloqueada.

---

## RB03. Uso de dados de irradiação
O cálculo de geração de energia deve utilizar obrigatoriamente os dados de irradiação solar obtidos para a localização do usuário.  
Caso esses dados não estejam disponíveis, o sistema não deve prosseguir com o cálculo.

---

## RB04. Limitação por área disponível
A quantidade de painéis solares deve ser limitada pela área disponível informada pelo usuário.  
O sistema deve impedir configurações que excedam essa área.

---

## RB05. Tipo de conexão elétrica
O cálculo deve considerar o tipo de conexão elétrica (monofásica, bifásica ou trifásica).  
Cada tipo deve aplicar sua respectiva taxa mínima de disponibilidade.

---

## RB06. Cálculo de Payback
O tempo de retorno (payback) deve ser calculado com base na comparação entre:  

- custo acumulado com energia da concessionária  
- investimento e economia gerada pelo sistema fotovoltaico  

---

## RB07. Atualização de tarifas
As tarifas de energia utilizadas no cálculo devem estar atualizadas conforme dados vigentes da ANEEL.  
Caso os dados estejam desatualizados, o sistema deve alertar o usuário.

---

## RB08. Validação de dados de entrada
O sistema deve validar todos os dados informados pelo usuário antes de iniciar o cálculo.  
Valores inconsistentes ou fora de faixa devem ser rejeitados.

---

## RB09. Limite de tempo de simulação
O cálculo completo da simulação deve ser finalizado em até 30 segundos.  
Caso esse tempo seja excedido, o sistema deve interromper o processo e informar o usuário.

---

## RB10. Exibição de resultados
O sistema só deve exibir o resultado final após todos os cálculos serem concluídos com sucesso.  
Resultados parciais ou incompletos não devem ser apresentados.
