# Caso de Uso 001
**Nome**: Realizar simulação de viabilidade solar

**Atores:** Usuário, Sistema SolarCalc

**Objetivo:** Permitir que o usuário simule a viabilidade financeira da instalação de um sistema fotovoltaico.

## Descrição

Este caso de uso descreve o processo em que o usuário insere seus dados de consumo, localização e características do imóvel para que o sistema calcule a geração de energia estimada e o tempo de retorno do investimento.

## Pré-condições
- o usuário deve acessar o sistema SolarCalc
- o sistema deve estar conectado às APIs externas necessárias

## Fluxo principal
1. O usuário acessa a página inicial do simulador.
2. O sistema exibe o formulário de simulação.
3. O usuário informa o consumo médio mensal de energia (kWh ou valor da conta).
4. O usuário informa o CEP da localização.
5. O usuário informa a área disponível do telhado (m²).
6. O usuário seleciona o tipo de conexão elétrica (monofásica, bifásica ou trifásica).
7. O usuário confirma a simulação.
8. O sistema consulta a Brasil API para converter o CEP em coordenadas geográficas.
9. O sistema consulta a NASA POWER API para obter o índice de irradiação solar.
10. O sistema consulta a Gemini API para obter dados de preços e marcas de painéis solares.
11. O sistema calcula a geração estimada de energia e o tempo de payback.
12. O sistema apresenta o resultado da simulação ao usuário.

## Fluxos alternativos
### A1. CEP inválido
1. No passo 8, o sistema identifica que o CEP informado é inválido.
2. O sistema informa o erro ao usuário.
3. O usuário corrige o CEP e reinicia a simulação.
### A2. Falha na comunicação com API
1. No passo 8, 9 ou 10 ocorre falha de comunicação com uma API.
2. O sistema informa que não foi possível concluir a simulação.
3. O sistema solicita que o usuário tente novamente mais tarde.

## Pós-condições
os resultados da simulação são exibidos ao usuário
os dados da simulação ficam disponíveis para visualização no dashboard


# Caso de Uso 002

**Nome:** Visualizar dashboard de resultados

**Atores:** Usuário, Sistema SolarCalc

**Objetivo:** Permitir que o usuário visualize os resultados da simulação de energia solar.

## Descrição

Este caso de uso descreve a visualização do dashboard que apresenta os resultados da simulação, incluindo geração estimada de energia, economia mensal e tempo de retorno do investimento.

## Pré-condições
- o usuário deve ter realizado uma simulação previamente
- o sistema deve ter calculado os resultados da simulação

## Fluxo principal
1. O sistema finaliza o cálculo da simulação.
2. O sistema gera os dados financeiros e energéticos.
3. O sistema apresenta um gráfico comparativo entre custos da concessionária e energia solar.
4. O sistema exibe o tempo estimado de payback.
5. O sistema apresenta a economia mensal estimada.
6. O usuário analisa os resultados exibidos no dashboard.

## Fluxos alternativos
### A1. Erro no cálculo
No passo 1 ocorre erro no processamento dos dados.
O sistema informa que não foi possível gerar os resultados.
O usuário pode tentar realizar a simulação novamente.

## Pós-condições
- o usuário obtém uma visão clara da viabilidade do investimento
- os resultados ficam disponíveis para análise

# Caso de Uso 003

**Nome:** Consultar dados de irradiação solar

**Atores:** Sistema SolarCalc, NASA POWER API

**Objetivo:** Obter dados de irradiação solar com base nas coordenadas do usuário.

## Descrição

Este caso de uso descreve o processo em que o sistema consulta a API da NASA para obter dados climáticos de irradiação solar necessários para o cálculo da geração de energia.

## Pré-condições
- o sistema deve possuir as coordenadas geográficas do usuário
- a API da NASA deve estar disponível

## Fluxo principal
1. O sistema recebe as coordenadas geográficas do usuário.
2. O sistema envia uma requisição para a NASA POWER API.
3. A API retorna os dados de irradiação solar da região.
4. O sistema armazena temporariamente os dados recebidos.
5. O sistema utiliza os dados no cálculo da geração de energia.

## Fluxos alternativos
### A1. API indisponível
1. No passo 2, a API não responde dentro do tempo limite.
2. O sistema registra a falha.
3. O sistema informa que não foi possível obter os dados climáticos.

## Pós-condições
- os dados de irradiação solar são disponibilizados para o cálculo da simulação

# Caso de Uso 004

**Nome:** Consultar preços de painéis solares

**Atores:** Sistema SolarCalc, Gemini API

**Objetivo:** Obter informações atualizadas sobre marcas e preços de painéis solares.

## Descrição
Este caso de uso descreve o processo em que o sistema consulta a Gemini API para obter dados atualizados sobre equipamentos fotovoltaicos.

## Pré-condições
- o sistema deve iniciar o cálculo da simulação
- a Gemini API deve estar disponível

## Fluxo principal
1. O sistema solicita dados de mercado de painéis solares.
2. O sistema envia uma requisição para a Gemini API.
3. A API retorna informações sobre marcas e preços médios.
4. O sistema utiliza esses dados para estimar o custo do sistema fotovoltaico.
5. O sistema inclui esses valores no cálculo de payback.

## Fluxos alternativos
### A1. Falha na API
1. No passo 2, a API não responde.
2. O sistema informa que não foi possível obter os preços atualizados.
3. O sistema sugere tentar novamente mais tarde.

## Pós-condições
- os dados de preços de painéis são utilizados no cálculo da simulação

# Caso de Uso 005

**Nome:** Gerenciar acesso do usuário (login, cadastro e recuperação de senha)

**Atores:** Usuário, Sistema SolarCalc

**Objetivo:** Permitir que o usuário crie uma conta, acesse o sistema e recupere sua senha quando necessário.

## Descrição

Este caso de uso descreve o processo de autenticação e gerenciamento de acesso do usuário, incluindo cadastro de nova conta, login no sistema e recuperação de senha em caso de esquecimento.

## Pré-condições
- o sistema SolarCalc deve estar disponível
- o usuário deve ter acesso à internet

## Fluxo principal (Login)
1. O usuário acessa a página de login.
2. O sistema exibe o formulário de autenticação.
3. O usuário informa e-mail e senha.
4. O usuário confirma o login.
5. O sistema valida as credenciais.
6. O sistema autentica o usuário.
7. O sistema redireciona o usuário para a página principal.

## Fluxos alternativos
### A1. Cadastro de novo usuário
1. No passo 1, o usuário seleciona a opção “criar conta”.
2. O sistema exibe o formulário de cadastro.
3. O usuário informa dados (nome, e-mail e senha).
4. O usuário confirma o cadastro.
5. O sistema valida os dados informados.
6. O sistema registra a nova conta.
7. O sistema informa sucesso e redireciona para login.

### A2. E-mail já cadastrado
1. No passo 5 do cadastro, o sistema identifica que o e-mail já existe.
2. O sistema informa que o usuário já possui conta.
3. O usuário pode tentar login ou recuperação de senha.

### A3. Recuperação de senha
1. passo 1, o usuário seleciona “esqueci minha senha”.
2. O sistema solicita o e-mail cadastrado.
3. O usuário informa o e-mail.
4. O sistema valida o e-mail.
5. O sistema envia instruções de redefinição de senha.
6. O usuário redefine a senha.
7. O sistema confirma a alteração.

### A4. Credenciais inválidas
1. No passo 5 do login, o sistema identifica dados incorretos.
2. O sistema informa erro de autenticação.
3. O usuário pode tentar novamente ou recuperar a senha.

### A5. Campos obrigatórios não preenchidos
1. No passo 5, o sistema detecta campos vazios.
2. O sistema solicita o preenchimento correto.
3. O usuário corrige os dados.

## Pós-condições
- o usuário está autenticado no sistema
- ou possui uma conta criada com sucesso
- ou redefine sua senha com sucesso