/**
 * NÚCLEO DO PROJETO — comunicação com a API e formatação de dados.
 */

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const STORAGE_SIMULACAO_ID = "simulacao_id";
const STORAGE_TOKEN = "token";
const STORAGE_SIMULACAO_ID_LEGADO = "solarcalc_simulacao_id";
const STORAGE_TOKEN_LEGADO = "solarcalc_token";
/** Senha padrão — autenticação fantasma do lead (formulário sem campo de senha). */
const senhaPadrao = "solarcalc2026";

/** Potência nominal por painel (kWp) — estimativa para exibição quando a API não envia qtd. */
const POTENCIA_PAINEL_KWP = 0.55;
/** Área média por painel (m²). */
const AREA_POR_PAINEL_M2 = 2;

/**
 * Recupera o ID da simulação da URL (?simulacao_id=) ou do localStorage.
 */
function salvarSimulacaoId(simulacaoId) {
    if (!simulacaoId) {
        return;
    }
    localStorage.setItem(STORAGE_SIMULACAO_ID, simulacaoId);
    localStorage.setItem(STORAGE_SIMULACAO_ID_LEGADO, simulacaoId);
}

function salvarToken(accessToken) {
    if (!accessToken) {
        return;
    }
    localStorage.setItem(STORAGE_TOKEN, accessToken);
    localStorage.setItem(STORAGE_TOKEN_LEGADO, accessToken);
}

function obterSimulacaoId() {
    const params = new URLSearchParams(window.location.search);
    const daUrl = params.get("simulacao_id");

    if (daUrl) {
        salvarSimulacaoId(daUrl);
        return daUrl;
    }

    return (
        localStorage.getItem(STORAGE_SIMULACAO_ID) ||
        localStorage.getItem(STORAGE_SIMULACAO_ID_LEGADO)
    );
}

function obterTokenAutenticacao() {
    return (
        localStorage.getItem(STORAGE_TOKEN) ||
        localStorage.getItem(STORAGE_TOKEN_LEGADO)
    );
}

function montarHeadersAutenticados(extraHeaders) {
    const headers = Object.assign({ Accept: "application/json" }, extraHeaders || {});
    const token = obterTokenAutenticacao();
    if (token) {
        headers.Authorization = "Bearer " + token;
    }
    return headers;
}

function parseValorReais(texto) {
    if (!texto) {
        return null;
    }
    const limpo = texto
        .replace(/[^\d,.-]/g, "")
        .replace(/\./g, "")
        .replace(",", ".");
    const numero = parseFloat(limpo);
    return Number.isFinite(numero) ? numero : null;
}

function normalizarCep(cep) {
    const digitos = (cep || "").replace(/\D/g, "");
    if (digitos.length !== 8) {
        return cep;
    }
    return digitos.slice(0, 5) + "-" + digitos.slice(5);
}

/**
 * Autenticação fantasma: registra (se necessário) e obtém JWT antes da simulação.
 */
async function autenticarPorEmail(nome, email) {
    await registrarLeadFantasma(nome, email);
    return await loginLeadFantasma(email);
}

/** POST /auth/register — ignora 400/409 (e-mail já cadastrado ou validação). */
async function registrarLeadFantasma(nome, email) {
    const resposta = await fetch(API_BASE_URL + "/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ nome: nome, email: email, senha: senhaPadrao }),
    });

    if (resposta.status === 400 || resposta.status === 409) {
        return;
    }

    if (!resposta.ok) {
        throw new Error("Não foi possível preparar sua conta para a simulação.");
    }
}

/** POST /auth/login — persiste access_token em localStorage antes de criar simulação. */
async function loginLeadFantasma(email) {
    const resposta = await fetch(API_BASE_URL + "/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ email: email, senha: senhaPadrao }),
    });

    if (!resposta.ok) {
        throw new Error("Falha na autenticação. Verifique o e-mail informado.");
    }

    const dados = await resposta.json();
    if (!dados.access_token) {
        throw new Error("Resposta de login inválida (sem token).");
    }

    localStorage.setItem("token", dados.access_token);
    salvarToken(dados.access_token);
    return dados.access_token;
}

async function criarEExecutarSimulacao(dadosFormulario) {
    const token = obterTokenAutenticacao();
    if (!token) {
        throw new Error("Autenticação necessária para iniciar a simulação.");
    }

    const valorReais = parseValorReais(dadosFormulario.gasto);
    if (!valorReais || valorReais <= 0) {
        throw new Error("Informe um gasto mensal válido.");
    }

    const payload = {
        valor_reais: valorReais,
        tipo_entrada: "REAIS",
        cep: normalizarCep(dadosFormulario.cep),
        area_m2: 50,
        orientacao: "NORTE",
        tipo_conexao: "MONOFASICA",
    };

    const headers = montarHeadersAutenticados({ "Content-Type": "application/json" });

    const criarResposta = await fetch(API_BASE_URL + "/simulacoes", {
        method: "POST",
        headers: headers,
        body: JSON.stringify(payload),
    });

    if (!criarResposta.ok) {
        throw new Error("Não foi possível iniciar a simulação.");
    }

    const simulacao = await criarResposta.json();
    const simulacaoId = simulacao.id || simulacao.simulacao_id;
    if (!simulacaoId) {
        throw new Error("Resposta da API sem identificador da simulação.");
    }

    const executarResposta = await fetch(
        API_BASE_URL + "/simulacoes/" + encodeURIComponent(simulacaoId) + "/executar",
        { method: "POST", headers: headers }
    );

    if (!executarResposta.ok) {
        throw new Error("Não foi possível concluir o cálculo da simulação.");
    }

    salvarSimulacaoId(simulacaoId);
    return simulacaoId;
}

/**
 * GET /api/v1/simulacoes/{simulacao_id} — retorna SimulacaoResultadoResponse.
 */
async function buscarSimulacaoConcluida(simulacaoId) {
    const token = obterTokenAutenticacao();
    if (!token) {
        throw new Error(
            "Sessão expirada. Volte ao simulador e conclua uma nova simulação."
        );
    }

    const headers = montarHeadersAutenticados();

    const resposta = await fetch(
        API_BASE_URL + "/simulacoes/" + encodeURIComponent(simulacaoId),
        { method: "GET", headers: headers }
    );

    if (!resposta.ok) {
        let detalhe = "Não foi possível carregar os resultados da simulação.";
        try {
            const erro = await resposta.json();
            if (erro.detail) {
                detalhe = typeof erro.detail === "string"
                    ? erro.detail
                    : JSON.stringify(erro.detail);
            }
        } catch (_e) {
            /* mantém mensagem padrão */
        }
        throw new Error(detalhe);
    }

    return resposta.json();
}

function parseNumero(valor) {
    if (valor === null || valor === undefined || valor === "") {
        return 0;
    }
    return typeof valor === "number" ? valor : parseFloat(valor);
}

/** R$ 1.234,56 */
function formatarMoedaBR(valor) {
    const numero = parseNumero(valor);
    return numero.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

/** Ex.: 3,42 */
function formatarDecimalBR(valor, casasDecimais) {
    const numero = parseNumero(valor);
    return numero.toLocaleString("pt-BR", {
        minimumFractionDigits: casasDecimais,
        maximumFractionDigits: casasDecimais,
    });
}

/** Converte payback decimal (anos) em texto legível. */
function formatarPaybackTexto(paybackAnosDecimal) {
    const total = parseNumero(paybackAnosDecimal);
    if (total <= 0) {
        return "—";
    }

    const anosInteiros = Math.floor(total);
    const meses = Math.round((total - anosInteiros) * 12);

    if (anosInteiros === 0) {
        return meses + (meses === 1 ? " mês" : " meses");
    }
    if (meses === 0) {
        return anosInteiros + (anosInteiros === 1 ? " ano" : " anos");
    }

    const labelAno = anosInteiros === 1 ? "ano" : "anos";
    const labelMes = meses === 1 ? "mês" : "meses";
    return anosInteiros + " " + labelAno + " e " + meses + " " + labelMes;
}

function estimarQuantidadePaineis(potenciaKwp) {
    const potencia = parseNumero(potenciaKwp);
    if (potencia <= 0) {
        return 0;
    }
    return Math.ceil(potencia / POTENCIA_PAINEL_KWP);
}

function estimarLucro25Anos(economiaMensal, investimento) {
    const economia = parseNumero(economiaMensal);
    const custo = parseNumero(investimento);
    return economia * 12 * 25 - custo;
}

/**
 * Monta projeção simplificada para o gráfico quando a API não envia série completa.
 */
function montarDadosGrafico(api) {
    const investimento = parseNumero(api.investimento);
    const consumo = parseNumero(api.consumo_kwh);
    const tarifa = parseNumero(api.tarifa_mock);
    const custoAnualConcessionaria = consumo * tarifa * 12;

    const anosLabels = [];
    const linhaConcessionaria = [];
    const linhaSolar = [];

    let acumuladoConcessionaria = 0;
    let acumuladoSolar = investimento;

    for (let ano = 0; ano <= 5; ano++) {
        anosLabels.push(ano);
        if (ano > 0) {
            acumuladoConcessionaria += custoAnualConcessionaria;
            acumuladoSolar += investimento * 0.01;
        }
        linhaConcessionaria.push(Math.round(acumuladoConcessionaria));
        linhaSolar.push(Math.round(acumuladoSolar));
    }

    return {
        anos_labels: anosLabels,
        linha_concessionaria: linhaConcessionaria,
        linha_solar: linhaSolar,
    };
}

/**
 * Adapta SimulacaoResultadoResponse ao formato consumido pelo dashboard.
 */
function mapearResultadoParaDashboard(api) {
    const potencia = parseNumero(api.potencia_kwp);
    const qtdPaineis = estimarQuantidadePaineis(potencia);
    const areaM2 = qtdPaineis * AREA_POR_PAINEL_M2;
    const lucro25 = estimarLucro25Anos(api.economia_mensal, api.investimento);

    return {
        resumo: {
            investimento: formatarMoedaBR(api.investimento),
            payback: formatarPaybackTexto(api.payback_anos),
            economia_mensal: formatarMoedaBR(api.economia_mensal),
            lucro_25_anos: formatarMoedaBR(lucro25),
        },
        tecnico: {
            potencia: formatarDecimalBR(potencia, 2) + " kWp",
            qtd_paineis: qtdPaineis + (qtdPaineis === 1 ? " painel" : " painéis"),
            area_telhado: "~ " + formatarDecimalBR(areaM2, 0) + " m²",
            marcas: "Consulte recomendações após integração completa",
        },
        grafico: montarDadosGrafico(api),
        bruto: api,
    };
}
