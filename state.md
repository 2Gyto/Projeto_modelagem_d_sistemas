# Registro de Estado — Solarcalc

[Executar Simulação — Motor com Mocks]
- Data: 29/05/2026

- Descrição: Implementado motor de cálculo simplificado na rota POST `/{simulacao_id}/executar` com tarifa_mock (0,83) e hsp_mock (4,5). Adicionadas `calcular_com_mocks` e `executar_calculo_mock` em `simulacao_service.py`, schema `SimulacaoResultadoResponse` em `schemas.py` e atualização da rota em `simulacoes.py`. A execução lê apenas o rascunho do banco e retorna JSON calculado, sem persistir resultado nem chamar APIs externas.

- Status: Concluído (Micro-etapa A - Lógica e Mocks).

[Persistência de Cálculos]
- Data: 29/05/2026

- Descrição: Integração do motor de cálculo com o SQLAlchemy para salvar os resultados financeiros na tabela `resultados` (potência, investimento/custo_total, economia, payback), atualizar `dados_consumo.consumo_kwh` quando derivado de reais, gravar mocks em `localizacoes` (HSP/tarifa) e marcar `simulacoes.status` como CONCLUIDA. A rota `POST /{simulacao_id}/executar` retorna `SimulacaoResultadoResponse` a partir da simulação persistida.

- Status: Concluído (Micro-etapa B - Persistência).

[Integração Front-end: Dashboard de Resultados]
- Data: 29/05/2026 03:40

- Descrição: Integração dos arquivos dashboard.js e nucleo__simulacao.js para consumir a API do backend, formatar os dados financeiros e renderizar os resultados reais na página resultado.html.

- Status: Concluído (Integração Front-end).

[Correção do fluxo de navegação]
- Data: 29/05/2026

- Descrição: Correção do fluxo de navegação: Implementado armazenamento do simulacao_id e Token no localStorage para garantir o carregamento do Dashboard. O wizard autentica via API, cria e executa a simulação, persiste `simulacao_id` e `token` antes do redirecionamento; o dashboard consome GET `/api/v1/simulacoes/{id}` com Bearer Token.

- Status: Concluído.

[Integração Completa APIs]
- Data: 29/05/2026

- Descrição: Integração Completa APIs: Brasil API (Geolocalização), Tarifas por UF, NASA (Radiação) e Gemini (Recomendação de Equipamentos). O `simulacao_service.py` consulta CEP, radiação climatológica e IA com fallbacks resilientes (tarifa 0,85, HSP 4,5, marcas Intelbras/WEG/Canadian Solar). A rota `POST /{simulacao_id}/executar` passou a usar `executar()` com persistência em `localizacoes` e `resultados`.

- Status: Concluído (Micro-etapa C - Integração APIs).
