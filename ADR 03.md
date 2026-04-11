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

