# ADR Nº 01

**Título:** Plataforma Web do Sistema SolarCalc
**Data:** 20 / 03 / 2026
**Responsável:** Gabriel Iunis
**Status:** Proposto

## Contexto

Descreva o problema que exigiu uma decisão técnica.  
Explique em que momento do projeto essa decisão apareceu e por que ela é importante.

**Perguntas que ajudam no preenchimento:**

- O que precisava ser decidido?
- Qual era a dúvida da equipe?
- Que necessidade do sistema motivou essa escolha?

## Decisão

Escreva de forma direta qual decisão foi tomada.

**Exemplos:**

- Foi escolhido o PostgreSQL como banco de dados do sistema.
- Foi adotada uma arquitetura em camadas.
- Foi definido o uso de API REST para comunicação entre frontend e backend.

## Justificativa

Explique por que essa decisão foi tomada.

**Pontos que podem aparecer:**

- melhor adequação ao problema
- simplicidade de implementação
- facilidade de manutenção
- desempenho
- segurança
- experiência da equipe
- prazo do projeto

## Alternativas consideradas

Liste outras opções avaliadas e explique, de forma breve, por que não foram escolhidas.

**Exemplos:**

- MySQL
- MongoDB
- Firebase

## Consequências

Descreva os efeitos da decisão.

Inclua:

- benefícios esperados
- limitações
- impactos para a equipe ou para o sistema

---

## Modelo para preencher

### Contexto

O projeto SolarCalc consiste em um sistema web que permite aos usuários avaliar a viabilidade da instalação de painéis solares em um imóvel. O sistema será acessado por meio de um site, no qual o usuário deverá criar uma conta e realizar login para utilizar as funcionalidades da plataforma.

Após acessar o sistema, o usuário poderá preencher um formulário com informações relevantes para a simulação, como consumo mensal de energia, localização do imóvel e características do telhado, incluindo orientação solar, inclinação, área disponível e presença de sombra.

Essas informações serão utilizadas pelo sistema para estimar a geração de energia solar e calcular indicadores financeiros como economia mensal e tempo de retorno do investimento (payback).


### Decisão

Foi decidido que o SolarCalc será desenvolvido exclusivamente como uma aplicação web acessada por meio de um site.

O sistema não terá versão mobile ou aplicativo dedicado para celulares ou tablets, sendo utilizado apenas através de navegadores de internet em computadores.

O site permitirá que usuários cadastrados realizem simulações informando dados do imóvel e do consumo de energia para receber uma análise de viabilidade da instalação de painéis solares.


### Justificativa

A escolha por uma aplicação web foi feita por ser a solução mais simples e adequada para o escopo do projeto.

Um sistema acessado por navegador facilita o desenvolvimento e a manutenção da aplicação, além de permitir que usuários utilizem a plataforma sem a necessidade de instalar aplicativos.

Além disso, essa abordagem reduz a complexidade do projeto e permite que a equipe foque no desenvolvimento da funcionalidade principal do sistema, que é a simulação da viabilidade da instalação de sistemas fotovoltaicos.


### Alternativas consideradas

- Desenvolvimento de uma planilha automatizada para cálculo da viabilidade solar 
- Desenvolvimento de uma aplicação desktop instalada no computador do usuário
- Utilização de calculadoras online simples sem sistema de autenticação



### Consequências

**Benefícios:**  
O sistema poderá ser acessado diretamente pelo navegador, sem necessidade de instalação de software adicional.

Além disso, o desenvolvimento focado em uma aplicação web simplifica o projeto e facilita a manutenção do sistema.


**Pontos de atenção:**  

Será necessário garantir que o site tenha uma interface clara e fácil de usar para os usuários.

Também será importante garantir que os cálculos de geração de energia e viabilidade financeira sejam baseados em dados confiáveis de incidência solar e parâmetros realistas de sistemas fotovoltaicos.

# ADR Nº 02

**Título:** Adoção de arquitetura monolítica para o SolarCalc  
**Data:** 20 / 03 / 2026 
**Responsável:** Gabriel Lopes Montalvão  
**Status:** Aceito  

## Contexto

Descreva o problema que exigiu uma decisão técnica.  
Explique em que momento do projeto essa decisão apareceu e por que ela é importante.

**Perguntas que ajudam no preenchimento:**

- O que precisava ser decidido?
- Qual era a dúvida da equipe?
- Que necessidade do sistema motivou essa escolha?

## Decisão

Escreva de forma direta qual decisão foi tomada.

**Exemplos:**

- Foi escolhido o PostgreSQL como banco de dados do sistema.
- Foi adotada uma arquitetura em camadas.
- Foi definido o uso de API REST para comunicação entre frontend e backend.

## Justificativa

Explique por que essa decisão foi tomada.

**Pontos que podem aparecer:**

- melhor adequação ao problema
- simplicidade de implementação
- facilidade de manutenção
- desempenho
- segurança
- experiência da equipe
- prazo do projeto

## Alternativas consideradas

Liste outras opções avaliadas e explique, de forma breve, por que não foram escolhidas.

**Exemplos:**

- MySQL
- MongoDB
- Firebase

## Consequências

Descreva os efeitos da decisão.

Inclua:

- benefícios esperados
- limitações
- impactos para a equipe ou para o sistema

---

## Modelo para preencher

### Contexto

Durante a fase inicial de definição da arquitetura do sistema SolarCalc, surgiu a necessidade de decidir qual modelo arquitetural seria utilizado para estruturar a aplicação.

O sistema é um simulador web que realiza cálculos de viabilidade de sistemas fotovoltaicos e depende da integração com APIs externas (Brasil API, NASA POWER API e Gemini API). Além disso, o projeto possui requisitos não funcionais relacionados a desempenho, usabilidade e confiabilidade, incluindo o limite de até 30 segundos para processamento completo da simulação.

Por se tratar de um projeto acadêmico com escopo limitado e sem previsão de uso em produção por grande quantidade de usuários, a equipe avaliou diferentes abordagens arquiteturais, considerando fatores como complexidade de implementação, facilidade de desenvolvimento e manutenção durante o período da disciplina.

A principal dúvida da equipe foi definir se seria mais adequado utilizar uma arquitetura mais complexa, como microserviços, ou uma estrutura mais simples que atendesse adequadamente às necessidades do projeto.

### Decisão

Foi decidido que o sistema SolarCalc será desenvolvido utilizando arquitetura monolítica, na qual todos os componentes da aplicação (interface, lógica de negócio, cálculos e integrações com APIs externas) serão executados dentro de uma única aplicação.

Apesar de ser monolítica, a aplicação será organizada internamente em camadas lógicas, como:

- camada de interface (frontend)
- camada de lógica de aplicação e cálculos
- camada de integração com APIs externas
- camada de acesso a dados

### Justificativa

A decisão pela arquitetura monolítica foi tomada considerando os seguintes fatores:

- simplicidade de implementação, adequada ao contexto acadêmico do projeto
- menor complexidade de infraestrutura, já que não será necessário gerenciar múltiplos serviços
- facilidade de manutenção
- facilidade de desenvolvimento e depuração, permitindo que a equipe trabalhe de forma mais direta no código
- tempo limitado da disciplina, que favorece soluções arquiteturais mais simples
- escala reduzida do sistema, já que o simulador não terá grande volume de usuários simultâneos

Além disso, a organização em camadas dentro do monólito permite manter uma boa separação de responsabilidades, facilitando manutenção e evolução do código sem introduzir complexidade arquitetural desnecessária.

### Alternativas consideradas

**Arquitetura de Microserviços**

Essa abordagem permitiria separar funcionalidades como cálculo, integração com APIs e geração de relatórios em serviços independentes.

No entanto, foi descartada devido a:

- aumento significativo de complexidade
- necessidade de orquestração entre serviço
- maior esforço de configuração e deploy
- pouca justificativa para um projeto de pequeno porte e acadêmico

**Arquitetura Serverless**

Foi considerada a possibilidade de implementar partes do sistema utilizando funções serverless para lidar com cálculos ou integrações externas.

Essa opção também foi descartada porque exigiria maior configuração de infraestrutura em nuvem e não traria benefícios significativos para o escopo do projeto.

### Consequências

**Benefícios:**  
- arquitetura simples e fácil de compreender
- desenvolvimento mais rápido para a equipe
- menor esforço de configuração e deploy
- facilidade de depuração durante o desenvolvimento
- menor complexidade de integração entre componentes

**Pontos de atenção:**  
- menor escalabilidade caso o sistema cresça significativamente
- necessidade de manter organização interna em camadas para evitar acoplamento excessivo
- futuras evoluções poderiam exigir refatoração para arquiteturas mais distribuídas caso o sistema evolua além do contexto acadêmico

\# ADR Nº 03



\*\*Título:\*\* Estratégia de tratamento de falhas das APIs externas  

\*\*Data:\*\* 20 / 03 / 2026  

\*\*Responsável:\*\* Gabriel Lopes Montalvão  

\*\*Status:\*\* Aceito 

\## Contexto



Descreva o problema que exigiu uma decisão técnica.  

Explique em que momento do projeto essa decisão apareceu e por que ela é importante.



\*\*Perguntas que ajudam no preenchimento:\*\*



\- O que precisava ser decidido?

\- Qual era a dúvida da equipe?

\- Que necessidade do sistema motivou essa escolha?



\## Decisão



Escreva de forma direta qual decisão foi tomada.



\*\*Exemplos:\*\*



\- Foi escolhido o PostgreSQL como banco de dados do sistema.

\- Foi adotada uma arquitetura em camadas.

\- Foi definido o uso de API REST para comunicação entre frontend e backend.



\## Justificativa



Explique por que essa decisão foi tomada.



\*\*Pontos que podem aparecer:\*\*



\- melhor adequação ao problema

\- simplicidade de implementação

\- facilidade de manutenção

\- desempenho

\- segurança

\- experiência da equipe

\- prazo do projeto



\## Alternativas consideradas



Liste outras opções avaliadas e explique, de forma breve, por que não foram escolhidas.



\*\*Exemplos:\*\*



\- MySQL

\- MongoDB

\- Firebase



\## Consequências



Descreva os efeitos da decisão.



Inclua:



\- benefícios esperados

\- limitações

\- impactos para a equipe ou para o sistema



\---



\## Modelo para preencher



\## Contexto



O sistema SolarCalc depende da integração com serviços externos para executar a simulação de viabilidade fotovoltaica. Durante o fluxo de cálculo, o sistema realiza requisições para:



\- Brasil API (conversão de CEP para coordenadas geográficas)

\- NASA POWER API (dados de irradiação solar)

\- Gemini API (informações de mercado sobre painéis solares)



Como esses serviços são externos ao sistema, existe a possibilidade de indisponibilidade temporária, latência elevada ou falhas de comunicação. Caso essas falhas não sejam tratadas adequadamente, a aplicação poderia travar ou apresentar comportamentos inesperados para o usuário.



Além disso, o sistema possui um requisito não funcional que determina que falhas de integração não devem causar o travamento da aplicação e devem ser comunicadas claramente ao usuário.



Diante disso, foi necessário definir uma estratégia de tratamento de falhas nas integrações com APIs externas.



\## Decisão



Foi decidido que o sistema implementará um mecanismo de \*\*tratamento de exceções e controle de timeout nas requisições às APIs externas\*\*.



As seguintes regras serão adotadas:



\- cada requisição para API externa terá \*\*tempo limite máximo de 10 segundos\*\*

\- caso a API não responda dentro desse tempo, a requisição será encerrada

\- o sistema exibirá \*\*uma mensagem clara informando que ocorreu uma falha temporária\*\*

\- o usuário será orientado a \*\*tentar novamente mais tarde\*\*

\- erros de integração serão registrados em logs para fins de depuração



\## Justificativa



A adoção dessa estratégia permite manter a aplicação estável mesmo em cenários de falha de serviços externos.



Os principais motivos para essa decisão foram:



\- evitar travamentos na interface do sistema

\- melhorar a experiência do usuário em situações de erro

\- permitir diagnóstico de problemas por meio de registros de log

\- manter o fluxo da aplicação previsível mesmo em caso de falhas externas



Como o sistema depende de múltiplas APIs externas, o tratamento adequado de exceções é essencial para garantir a confiabilidade da aplicação.



\## Alternativas consideradas



\*\*Não tratar falhas explicitamente\*\*



Essa abordagem consistiria em deixar o sistema lidar automaticamente com exceções de rede ou falhas de API.



Essa opção foi descartada porque poderia causar:



\- travamentos inesperados

\- mensagens de erro técnicas incompreensíveis para o usuário

\- interrupção do fluxo da aplicação



\*\*Implementar sistema avançado de retry automático\*\*

a

Foi considerada a possibilidade de implementar múltiplas tentativas automáticas de requisição.



Essa opção foi descartada porque poderia aumentar o tempo total de resposta da simulação e ultrapassar o limite de tempo definido para o processamento.



\## Consequências



\### Benefícios



\- maior estabilidade da aplicação

\- melhor experiência do usuário em casos de falha

\- controle sobre tempo máximo de espera das integrações

\- possibilidade de diagnóstico por meio de logs



\### Pontos de atenção



\- falhas temporárias das APIs ainda impedirão a conclusão da simulação

\- o sistema depende da disponibilidade dos serviços externos para funcionar completamente


# ADR Nº 04

**Título:** Uso de autenticação de usuários no sistema SolarCalc  
**Data:** 20 / 03 / 2026
**Responsável:** Gabriel Iunis
**Status:** Proposto

## Contexto

Descreva o problema que exigiu uma decisão técnica.  
Explique em que momento do projeto essa decisão apareceu e por que ela é importante.

**Perguntas que ajudam no preenchimento:**

- O que precisava ser decidido?
- Qual era a dúvida da equipe?
- Que necessidade do sistema motivou essa escolha?

## Decisão

Escreva de forma direta qual decisão foi tomada.

**Exemplos:**

- Foi escolhido o PostgreSQL como banco de dados do sistema.
- Foi adotada uma arquitetura em camadas.
- Foi definido o uso de API REST para comunicação entre frontend e backend.

## Justificativa

Explique por que essa decisão foi tomada.

**Pontos que podem aparecer:**

- melhor adequação ao problema
- simplicidade de implementação
- facilidade de manutenção
- desempenho
- segurança
- experiência da equipe
- prazo do projeto

## Alternativas consideradas

Liste outras opções avaliadas e explique, de forma breve, por que não foram escolhidas.

**Exemplos:**

- MySQL
- MongoDB
- Firebase

## Consequências

Descreva os efeitos da decisão.

Inclua:

- benefícios esperados
- limitações
- impactos para a equipe ou para o sistema

---

## Modelo para preencher

### Contexto

O sistema SolarCalc permite que usuários realizem simulações de viabilidade para instalação de painéis solares com base em dados como consumo de energia, localização e características do telhado.

Durante o desenvolvimento, surgiu a necessidade de definir se o sistema exigiria autenticação de usuários ou se permitiria o uso livre sem cadastro.

Essa decisão impacta diretamente na forma como os dados são armazenados, na personalização da experiência do usuário e na possibilidade de manter um histórico de simulações realizadas.

### Decisão

Foi decidido que o sistema SolarCalc exigirá autenticação de usuários, sendo necessário que o usuário realize cadastro e login para utilizar a plataforma.

Cada usuário terá sua conta individual e poderá acessar suas simulações previamente realizadas.


### Justificativa

A autenticação permite associar as simulações a um usuário específico, possibilitando o armazenamento e consulta de histórico.

Além disso, melhora a organização dos dados e permite uma experiência mais personalizada, como a criação de um dashboard com resultados anteriores.

Essa abordagem também facilita futuras expansões do sistema, como recomendações personalizadas ou comparação entre simulações.


### Alternativas consideradas

- Autenticação por e-mail e senha;
- Autenticação por conta Google;
- Autenticação por e-mail institucional ou identificador único.



### Consequências

**Benefícios:**  

Permite armazenar o histórico de simulações de cada usuário.

Possibilita a criação de funcionalidades personalizadas, como dashboards e acompanhamento de análises.

Melhora a organização e segurança dos dados do sistema.

**Pontos de atenção:**  

Será necessário implementar mecanismos de segurança para proteção de dados de login, como armazenamento seguro de senhas.

Também será necessário gerenciar autenticação e sessões de usuários dentro do sistema.

# ADR Nº 05

**Título:** Seleção das APIs externas para geolocalização, dados climáticos e precificação de equipamentos  
**Data:** 24/04/2026  
**Responsável:** Arthur De Almeida Santos  
**Status:** Aceito

---

## Contexto

O SolarCalc depende de três categorias de dados externos para executar a simulação de viabilidade fotovoltaica:

1. **Geolocalização** — converter o CEP do usuário em coordenadas geográficas (latitude e longitude) para determinar a localização precisa do imóvel.
2. **Dados de irradiação solar** — obter o índice HSP (Horas de Pico de Sol) da região com base nas coordenadas geográficas, dado essencial para estimar a geração de energia.
3. **Preços e marcas de painéis solares** — obter valores de mercado atualizados para painéis fotovoltaicos, evitando que o sistema trabalhe com dados defasados.

A equipe precisou decidir quais serviços e APIs seriam utilizados para cada uma dessas três necessidades, considerando disponibilidade, custo, precisão dos dados, facilidade de integração e adequação ao contexto brasileiro.

---

## Decisão

Foram selecionadas as seguintes APIs para cada necessidade:

| Necessidade | API Selecionada | Endpoint principal |
|------------|----------------|-------------------|
| Geolocalização (CEP → coordenadas) | **Brasil API** | `brasilapi.com.br/api/cep/v2/{cep}` |
| Índice de irradiação solar (HSP) | **NASA POWER API** | `power.larc.nasa.gov/api/temporal/monthly/...` |
| Preços e marcas de painéis | **Google Gemini API** | `generativelanguage.googleapis.com/v1beta/models/gemini-pro` |

Todas as integrações serão realizadas no backend, com timeout máximo de 10 segundos por requisição, conforme [ADR Nº 03](ADRs.md#adr-03).

---

## Justificativa

### Brasil API (Geolocalização)
- Serviço gratuito e específico para o mercado brasileiro, com excelente cobertura de CEPs nacionais
- Retorna latitude e longitude diretamente no response, sem necessidade de processamento adicional
- Não requer chave de API para uso básico, reduzindo complexidade de configuração
- Documentação em português e comunidade ativa no Brasil
- Alternativa ao Google Maps Geocoding API que exigiria cobrança após volume de requisições

### NASA POWER API (Irradiação Solar)
- Dados científicos validados pela NASA com cobertura global e histórico de mais de 30 anos
- Fornece o índice de irradiação solar (HSP) especificamente para coordenadas geográficas, com granularidade mensal e anual
- API pública e gratuita, sem necessidade de cadastro ou chave de autenticação para uso padrão
- Os dados são amplamente utilizados pela indústria fotovoltaica e reconhecidos como referência técnica
- Permite consulta por parâmetro `ALLSKY_SFC_SW_DWN` que representa a irradiação global horizontal — base do cálculo de geração fotovoltaica

### Google Gemini API (Preços de Painéis)
- Capacidade de busca e síntese de informações de mercado atualizadas, eliminando o problema de dados defasados em bancos de dados estáticos
- Permite consultas em linguagem natural sobre marcas, modelos e preços de painéis no mercado brasileiro
- Integração via SDK oficial do Google com boa documentação
- Evita a necessidade de manter e atualizar manualmente uma base de dados de equipamentos
- Permite parametrizar as consultas para filtrar por potência, preço e disponibilidade no mercado nacional

---

## Alternativas Consideradas

### Para Geolocalização (CEP → Coordenadas)

**Google Maps Geocoding API**  
Rejeitada por: exige chave de API paga após volume de requisições, custo desnecessário para um projeto acadêmico de pequeno porte.

**ViaCEP**  
Rejeitada por: retorna apenas dados de endereço (logradouro, cidade, estado), sem coordenadas geográficas — exigiria uma segunda chamada para obter lat/lng.

**OpenStreetMap Nominatim**  
Rejeitada por: politica de uso proíbe uso em produção com volume de requisições sem hospedagem própria; latência mais alta que a Brasil API para CEPs brasileiros.

---

### Para Irradiação Solar (HSP)

**INMET (Instituto Nacional de Meteorologia)**  
Rejeitado por: API com documentação limitada, cobertura de estações irregulares no interior do país e dados históricos menos abrangentes que a NASA POWER.

**Solargis**  
Rejeitado por: serviço pago com planos a partir de valores significativos mensais, inviável para o escopo acadêmico do projeto.

**SolarAnywhere**  
Rejeitado por: API proprietária paga sem plano gratuito adequado ao volume de consultas do projeto.

---

### Para Preços de Painéis Solares

**Banco de dados interno (tabela estática)**  
Rejeitado por: exigiria atualização manual periódica e os dados ficariam rapidamente defasados, comprometendo a credibilidade das simulações.

**Web scraping de sites de distribuidores**  
Rejeitado por: instabilidade dos seletores HTML, risco de bloqueio por parte dos sites e questões legais relacionadas à extração de dados sem autorização.

**OpenAI GPT-4**  
Considerada como alternativa ao Gemini, foi preterida por: custo por token mais elevado e ausência de integração nativa com busca em tempo real no plano padrão.

---

## Consequências

### Benefícios
- As três APIs cobrindo necessidades distintas criam um pipeline de dados robusto e especializado para cada função
- Uso de APIs gratuitas (Brasil API e NASA POWER) e modelo de consumo controlado (Gemini) mantém o custo operacional baixo
- Dados da NASA conferem credibilidade técnica ao sistema, um diferencial competitivo relevante
- O Gemini elimina a necessidade de manutenção de base de dados de equipamentos

### Pontos de Atenção
- O sistema depende da disponibilidade simultânea das três APIs para concluir uma simulação; falhas em qualquer uma bloqueiam o resultado (mitigado pelo [ADR Nº 03](ADRs.md#adr-03))
- A Gemini API tem custo por requisição após o limite gratuito mensal — deve-se monitorar o uso
- Os dados retornados pelo Gemini são estimativas baseadas em linguagem; devem ser tratados como valores de referência, não como cotações oficiais
- A NASA POWER API pode apresentar latência variável dependendo da carga do servidor

---

## Referências Cruzadas

| Documento | Seção | Relação |
|-----------|-------|---------|
| [RNF01](RNFs.md#rnf01) | Desempenho | Define o limite de 30s incluindo todas as chamadas de API |
| [RNF05](RNFs.md#rnf05) | Tolerância a Falhas | Define comportamento em caso de falha de API |
| [RB02](RB.md#rb02) | Conversão de localização | Define regra para CEP inválido |
| [RB03](RB.md#rb03) | Dados de irradiação | Obrigatoriedade dos dados da NASA |
| [ADR Nº 03](ADRs.md#adr-03) | Tratamento de falhas | Estratégia de timeout e mensagens de erro |
| [RF02](RF.md#rf02) | Localização Geográfica | Requisito funcional de geolocalização |

---

# ADR Nº 06

**Título:** Estratégia de persistência de dados e banco de dados do SolarCalc  
**Data:** 24/04/2026  
**Responsável:** Gabriel Andre Iunis De Paula  
**Status:** Aceito

---

## Contexto

O sistema SolarCalc, conforme [ADR Nº 04](ADRs.md#adr-04), exige autenticação de usuários e armazenamento do histórico de simulações. Isso implica a necessidade de persistir:

1. **Dados de usuário** — credenciais de acesso e perfil
2. **Histórico de simulações** — parâmetros informados e resultados gerados
3. **Tarifas de concessionárias** — dados da ANEEL que precisam ser atualizados mensalmente

A equipe precisou decidir qual tecnologia de banco de dados utilizar, o modelo de armazenamento dos dados das simulações e a estratégia de atualização das tarifas ANEEL.

Considerando que o sistema adota arquitetura monolítica ([ADR Nº 02](ADRs.md#adr-02)) e que o escopo é acadêmico com volume baixo de usuários simultâneos, buscou-se uma solução simples, madura e adequada ao contexto relacional dos dados.

---

## Decisão

Foi decidido que o SolarCalc utilizará **PostgreSQL** como banco de dados relacional para persistência de todos os dados da aplicação.

A estrutura de dados adotará o seguinte modelo:

| Tabela | Conteúdo principal |
|--------|-------------------|
| `usuarios` | id, nome, email, senha_hash, criado_em |
| `simulacoes` | id, usuario_id, status, realizada_em |
| `dados_consumo` | id, simulacao_id, consumo_kwh, valor_reais, tipo_entrada |
| `localizacoes` | id, simulacao_id, cep, cidade, latitude, longitude |
| `dados_telhado` | id, simulacao_id, area_m2, orientacao, tipo_conexao |
| `resultados` | id, simulacao_id, geracao_kwh, economia_mensal, payback_anos, payback_meses, custo_total |
| `projecoes_anuais` | id, resultado_id, ano, custo_concessionaria, custo_fotovoltaico, saldo |
| `tarifas_concessionarias` | id, concessionaria, tarifa_kwh, taxa_mono, taxa_bi, taxa_tri, atualizado_em, resolucao_aneel |

As senhas de usuários serão armazenadas com hash usando **bcrypt** com salt aleatório — nunca em texto plano.

---

## Justificativa

**PostgreSQL foi escolhido pelos seguintes motivos:**

- **Maturidade e confiabilidade** — banco de dados relacional robusto com décadas de uso em produção
- **Natureza relacional dos dados** — simulações, usuários, resultados e tarifas possuem relacionamentos bem definidos que se beneficiam de chaves estrangeiras e integridade referencial
- **Suporte a tipos de dados avançados** — arrays, JSONB e funções de data facilitam o armazenamento de projeções e cálculos de 25 anos
- **Gratuito e open-source** — sem custo de licença
- **Ampla adoção no mercado** — facilidade de encontrar documentação, tutoriais e suporte
- **Compatibilidade com ORMs populares** — integração direta com frameworks como Django, Spring Boot, Prisma e outros que a equipe pode utilizar

---

## Alternativas Consideradas

**MySQL / MariaDB**  
Considerado e preterido por: PostgreSQL possui suporte mais robusto a tipos de dados avançados (JSONB, arrays) e conformidade mais estrita com o padrão SQL. Para este projeto, ambos seriam viáveis, mas o PostgreSQL foi escolhido pela experiência da equipe e recursos adicionais.

**MongoDB (banco de documentos NoSQL)**  
Rejeitado por: os dados do SolarCalc possuem estrutura relacional bem definida (usuário → simulações → resultados → projeções), que se beneficia de chaves estrangeiras e integridade referencial. Um banco de documentos adicionaria complexidade desnecessária para garantir consistência dos dados.

**Firebase Realtime Database / Firestore**  
Rejeitado por: solução proprietária do Google que introduz dependência de vendor. Além disso, o modelo de cobrança por leitura/escrita pode ser imprevisível, e as capacidades de consulta relacional são limitadas para relatórios comparativos.

**SQLite**  
Considerado para desenvolvimento local, mas rejeitado como banco de produção por: limitações de concorrência (um escritor por vez), ausência de suporte robusto a múltiplos usuários simultâneos e menor capacidade de escalonamento.

---

## Consequências

### Benefícios
- Integridade referencial garantida pelo banco — simulações sempre vinculadas a usuários válidos, resultados sempre vinculados a simulações concluídas
- Consultas SQL expressivas para geração de relatórios comparativos e histórico de simulações
- Fácil manutenção e atualização das tarifas ANEEL diretamente na tabela `tarifas_concessionarias`
- Senhas protegidas com bcrypt — conformidade com boas práticas de segurança
- Facilidade de backup e restauração com ferramentas nativas do PostgreSQL (`pg_dump`)

### Pontos de Atenção
- Requer instalação e configuração de um servidor PostgreSQL (local ou em nuvem)
- A atualização mensal das tarifas ANEEL precisa de processo definido (manual ou automatizado via script)
- Migração do schema de banco de dados deve ser gerenciada com cuidado à medida que o sistema evoluir
- Em ambiente de produção real, seria necessário configurar backups automáticos e monitoramento

### Processo de Atualização de Tarifas
Conforme [RB07](RB.md#rb07) e [RNF04](RNFs.md#rnf04), as tarifas devem ser atualizadas mensalmente. O processo será:
1. Consultar as resoluções vigentes da ANEEL
2. Executar script de atualização na tabela `tarifas_concessionarias`
3. Registrar o número da resolução e a data de atualização
4. O sistema verificará a data de `atualizado_em` e alertará o usuário caso esteja há mais de 35 dias sem atualização

---

## Referências Cruzadas

| Documento | Seção | Relação |
|-----------|-------|---------|
| [ADR Nº 02](ADRs.md#adr-02) | Arquitetura monolítica | Define o contexto arquitetural que orienta a escolha do banco |
| [ADR Nº 04](ADRs.md#adr-04) | Autenticação de usuários | Define a necessidade de persistir dados de usuário e histórico |
| [RB07](RB.md#rb07) | Atualização de tarifas | Regra de negócio que exige processo de atualização mensal |
| [RB08](RB.md#rb08) | Validação de dados | Integridade referencial do banco reforça as validações da aplicação |
| [RNF04](RNFs.md#rnf04) | Confiabilidade e padronização | Define frequência de atualização das tarifas ANEEL |
| [ModeloDominio.md](ModeloDominio.md) | Entidades do domínio | As tabelas do banco refletem diretamente o modelo de domínio |
