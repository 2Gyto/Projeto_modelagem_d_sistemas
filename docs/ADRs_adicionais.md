# ADRs Adicionais — SolarCalc

**Versão:** 1.0  
**Data:** 24/04/2026  
**Complemento ao documento:** [ADRs.md](ADRs.md) (ADR Nº 01 a 04)

---

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
