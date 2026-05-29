// static/js/dashboard.js

const IDS_CAMPOS_RESULTADO = [
    "txt-investimento",
    "txt-payback",
    "txt-economia",
    "txt-lucro",
    "txt-potencia",
    "txt-paineis",
    "txt-area",
    "txt-marcas",
];

const TEXTO_CARREGANDO = "Carregando dados...";

function definirEstadoCarregamento(ativo) {
    IDS_CAMPOS_RESULTADO.forEach(function (id) {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = ativo ? TEXTO_CARREGANDO : "--";
        }
    });
}

function preencherDashboard(dados) {
    document.getElementById("txt-investimento").textContent = dados.resumo.investimento;
    document.getElementById("txt-payback").textContent = dados.resumo.payback;
    document.getElementById("txt-economia").textContent = dados.resumo.economia_mensal;
    document.getElementById("txt-lucro").textContent = dados.resumo.lucro_25_anos;

    document.getElementById("txt-potencia").textContent = dados.tecnico.potencia;
    document.getElementById("txt-paineis").textContent = dados.tecnico.qtd_paineis;
    document.getElementById("txt-area").textContent = dados.tecnico.area_telhado;
    document.getElementById("txt-marcas").textContent = dados.tecnico.marcas;
}

function renderizarGraficoPayback(dados) {
    const canvas = document.getElementById("graficoPayback");
    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: dados.grafico.anos_labels,
            datasets: [
                {
                    label: "Custo sem Energia Solar (Conta de Luz)",
                    data: dados.grafico.linha_concessionaria,
                    borderColor: "#dc3545",
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.1,
                },
                {
                    label: "Custo Acumulado com Solar",
                    data: dados.grafico.linha_solar,
                    borderColor: "#FF6B00",
                    backgroundColor: "rgba(255, 107, 0, 0.1)",
                    fill: true,
                    tension: 0.1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return formatarMoedaBR(context.parsed.y);
                        },
                    },
                },
            },
            scales: {
                y: {
                    ticks: {
                        callback: function (valor) {
                            return formatarMoedaBR(valor);
                        },
                    },
                },
            },
        },
    });
}

function exibirErroCarregamento(mensagem) {
    IDS_CAMPOS_RESULTADO.forEach(function (id) {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = "—";
        }
    });

    const alerta = document.getElementById("alerta-erro-dashboard");
    if (alerta) {
        alerta.textContent = mensagem;
        alerta.classList.remove("d-none");
    } else {
        console.error(mensagem);
        alert(mensagem);
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const nome = urlParams.get("nome");
    if (nome) {
        document.getElementById("nomeUsuario").textContent = nome;
    }

    const simulacaoId = obterSimulacaoId();
    if (!simulacaoId) {
        exibirErroCarregamento(
            "Simulação não encontrada. Volte ao simulador e conclua uma simulação."
        );
        return;
    }

    definirEstadoCarregamento(true);

    try {
        const resultadoApi = await buscarSimulacaoConcluida(simulacaoId);
        const dados = mapearResultadoParaDashboard(resultadoApi);
        preencherDashboard(dados);
        renderizarGraficoPayback(dados);
    } catch (erro) {
        console.error("Erro ao carregar simulação:", erro);
        exibirErroCarregamento(erro.message || "Falha ao carregar os resultados.");
    }
});
