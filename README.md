# Documento de Visão do Produto

## 1. Identificação do Produto
Nome do produto: SolarCalc - Simulador de Viabilidade Fotovoltaica

Versão do documento: 1.1

Data: 12/03/2026

Equipe responsável:
- Arthur De Almeida Santos
- Gabriel Andre Iunis De Paula
- Gabriel Lopes Montalvao


## 2. Visão Geral
O SolarCalc é um simulador web voltado ao cálculo de viabilidade e tempo real de retorno (Payback) para investimentos em energia solar fotovoltaica.

O sistema busca trazer transparência e precisão para o consumidor, considerando fatores reais de localização, tarifas e custos atualizados de equipamentos, oferecendo uma projeção financeira clara do investimento com o apoio de inteligência artificial.

## 3. Problema
Muitos proprietários investem em energia solar sem entender o tempo real de retorno do investimento (Payback). As decisões muitas vezes baseiam-se em estimativas vagas que ignoram fatores críticos, como o índice de irradiação exato do local, taxas específicas da concessionária e a variação constante de preços e marcas de equipamentos no mercado.

Isso gera incerteza financeira, expectativas frustradas e dificuldade na tomada de decisão sobre a instalação do sistema.

## 4. Objetivo do Produto
O produto tem como objetivo:

- calcular a viabilidade financeira e o tempo de retorno (Payback) de sistemas fotovoltaicos

- estimar a geração mensal de energia com base em coordenadas geográficas e dados climáticos da NASA

- comparar os custos acumulados com a concessionária versus o custo do sistema solar

- prover dados precisos de custos e marcas de painéis utilizando inteligência artificial

## 5. Público-Alvo
O sistema é destinado principalmente a:

- proprietários residenciais

- pequenos comerciantes

## 6. Principais Necessidades dos Usuários
### Proprietários Residenciais
- reduzir o valor da conta de luz (economia doméstica)

- valorizar o seu imóvel

- entender de forma simples em quanto tempo o sistema se paga

- ter uma noção realista dos preços dos painéis disponíveis no mercado

### Pequenos Comerciantes
- reduzir o custo operacional do negócio (OPEX)

- obter previsibilidade de caixa a longo prazo

- comparar de forma clara os cenários com e sem energia solar

## 7. Proposta de Valor
O sistema oferece uma simulação financeira e técnica precisa, baseada em dados espaciais globais e inteligência artificial, permitindo que o usuário visualize com clareza o retorno do seu investimento.

Em vez de depender de orçamentos enviesados de vendedores, o produto fornece autonomia, transparência sobre os custos reais dos equipamentos e segurança na decisão de investir em energia solar.

## 8. Funcionalidades Principais
- coleta de dados de consumo (média em kWh ou valor em Reais)

- conversão de CEP em coordenadas geográficas (latitude/longitude) via Brasil API

- busca de índices precisos de irradiação solar (HSP) baseados nas coordenadas via NASA POWER API

- levantamento dinâmico de preços médios e marcas recomendadas de painéis solares via Gemini API

- especificação de área disponível (m²) e orientação do telhado

- seleção de perfil de conexão (Monofásica, Bifásica ou Trifásica)

- cálculo de geração estimada de energia e estimativa de Payback (em anos e meses)

- dashboard de gráfico comparativo de custos (concessionária vs. fotovoltaico)

## 9. Benefícios Esperados
- maior segurança na decisão de investimento

- estimativas de geração de energia altamente precisas com dados validados pela NASA

- transparência sobre os custos reais dos equipamentos utilizando dados atualizados por IA

- agilidade na obtenção de uma análise de viabilidade confiável

## 10. Restrições e Premissas
### Restrições
- o sistema será uma aplicação web responsiva

- o fluxo de preenchimento deve ter no máximo 5 etapas

- o cálculo de projeção de 25 anos deve ocorrer em até 30 segundos

- o design dos gráficos deve ser acessível para daltônicos e ter legendas claras

- uso exclusivo do padrão monetário brasileiro (BRL) e sistema métrico decimal

### Premissas
- o usuário tem acesso aos dados de sua conta de luz (consumo ou valor pago)

- haverá disponibilidade e tempo de resposta adequado das APIs de terceiros (Brasil API, NASA POWER e Gemini API)

- os dados de tarifas precisam ser atualizados mensalmente conforme resoluções da ANEEL

## 11. Diferenciais do Produto
- Geolocalização Inteligente: Uso da Brasil API para converter o CEP do usuário em coordenadas exatas de forma transparente.

- Dados Climáticos de Alta Precisão: Integração com a NASA POWER API, garantindo índices de irradiação solar globais e validados cientificamente.

- Orçamento Dinâmico com IA: Utilização da Gemini API para buscar ativamente informações sobre marcas e preços de mercado dos painéis, evitando que o sistema fique com valores defasados.

- cálculo que considera a taxa de disponibilidade por tipo de conexão (mono/bi/trifásica).

## 12. Critérios de Sucesso
O produto será considerado bem-sucedido se:

- os usuários conseguirem concluir a simulação sem abandonar o fluxo (máximo de 5 etapas)

- a comunicação entre as 3 APIs (Brasil API -> NASA POWER -> Gemini) ocorrer de forma fluida e abaixo de 30 segundos

- as estimativas geradas refletirem com precisão a realidade de mercado e as tarifas da ANEEL

## 13. Escopo Inicial
O escopo inicial do produto inclui:

- cálculo de viabilidade e ROI

- fluxo de geolocalização (CEP para Coordenadas via Brasil API)

- integração com a NASA POWER API para índices de irradiação

- integração com a Gemini API para consulta de dados de equipamentos

- suporte às tarifas das concessionárias brasileiras

- dashboard comparativo responsivo

## 14. Fora do Escopo Inicial
Nesta primeira versão, não fazem parte do escopo:

- venda direta de equipamentos fotovoltaicos

- elaboração de projeto de engenharia para submissão à concessionária

- monitoramento em tempo real do sistema pós-instalação

## 15. Resumo Executivo
O SolarCalc é um simulador web que traz transparência para o mercado de energia fotovoltaica. Ao cruzar dados de consumo com coordenadas geográficas exatas (Brasil API), dados climáticos da agência espacial americana (NASA POWER API) e inteligência artificial para cotação de equipamentos (Gemini API), o sistema permite que proprietários e comerciantes calculem a viabilidade e o tempo de retorno de seus investimentos de forma rápida, acessível e segura, eliminando a incerteza antes da compra.

## Como rodar o projeto (rápido)

### Usando Docker Compose (recomendado)

1. No diretório raiz do projeto rode:

```powershell
docker-compose up --build
```

2. A API ficará disponível em `http://localhost:8000` e o frontend será servido em `http://localhost:8000/app`.

### Rodando localmente (sem Docker)

1. Crie e ative um ambiente virtual Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
pip install -r src/backend/requirements.txt
```

2. Gere o banco de tarifas (SQLite) e/ou configure o PostgreSQL conforme necessário:

```powershell
# cria/atualiza src/backend/data/tarifas_uf.db
python src/backend/scripts/seed_tarifas_uf.py

# (opcional) Para usar PostgreSQL, exporte a variável DATABASE_URL apontando para seu container/postgres
$env:DATABASE_URL = 'postgresql+psycopg://solarcalc:solarcalc@localhost:5432/solarcalc'
```

3. Rode a API:

```powershell
cd src/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Abra o frontend em `http://localhost:8000/app`.

Se quiser, eu posso adaptar o `docker-compose.yml` para rodar também um serviço front separado (por exemplo, um servidor estático Nginx) ou incluir variáveis de ambiente adicionais para produção.
