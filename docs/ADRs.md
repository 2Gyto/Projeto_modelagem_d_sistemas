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
