const API_BASE = "/api/v1";

const fmtBRL = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
});
const fmtNum = new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

document.addEventListener("DOMContentLoaded", async () => {
    const carregando = document.getElementById("estadoCarregando");
    const erroBox = document.getElementById("estadoErro");
    const ok = document.getElementById("estadoOk");

    const id = new URLSearchParams(window.location.search).get("id");
    if (!id) {
        mostrarErro("Simulação não informada na URL.");
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE}/simulacoes/publica/${id}`);
        if (!resposta.ok) {
            const detalhe = await resposta.json().catch(() => ({}));
            throw new Error(detalhe.detail || "Simulação não encontrada.");
        }
        const dados = await resposta.json();
        
        preencherResultado(dados);
        renderizarGrafico(dados); // Chamada da nova função do gráfico
        
        carregando.classList.add("d-none");
        ok.classList.remove("d-none");
    } catch (err) {
        mostrarErro(err.message);
    }

    function mostrarErro(msg) {
        carregando.classList.add("d-none");
        erroBox.innerText = msg;
        erroBox.classList.remove("d-none");
    }
});

function preencherResultado(d) {
    document.getElementById("saudacaoNome").innerText = (d.nome || "").split(" ")[0];
    document.getElementById("dadoCep").innerText = d.cep;
    document.getElementById("dadoGasto").innerText = fmtBRL.format(Number(d.valor_reais));

    document.getElementById("resultadoPaineis").innerText = d.quantidade_paineis;
    document.getElementById("resultadoConsumo").innerText = fmtNum.format(Number(d.consumo_kwh_mes));
    document.getElementById("resultadoPotencia").innerText = fmtNum.format(Number(d.potencia_sistema_kwp));
    document.getElementById("resultadoGeracao").innerText = fmtNum.format(Number(d.geracao_total_kwh_mes));
    document.getElementById("resultadoEconomia").innerText = fmtBRL.format(Number(d.economia_mensal_reais));
}

// Lógica Ninja para criar a projeção financeira
function renderizarGrafico(d) {
    const canvas = document.getElementById("graficoProjecao");
    if (!canvas) {
        console.warn("Canvas do gráfico não encontrado no HTML. Crie uma tag <canvas id='graficoProjecao'></canvas> no seu HTML.");
        return;
    }

    const anos = 25;
    const labels = [];
    const dadosEconomia = [];
    let economiaAcumulada = 0;
    
    // Calcula a economia anual baseada na mensal
    const economiaAnual = Number(d.economia_mensal_reais) * 12;

    for (let i = 1; i <= anos; i++) {
        labels.push(`Ano ${i}`);
        economiaAcumulada += economiaAnual;
        dadosEconomia.push(economiaAcumulada);
    }

    new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Economia Acumulada (R$)',
                data: dadosEconomia,
                borderColor: '#10b981', // Verde tecnológico
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.3 // Deixa a linha suave
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return fmtBRL.format(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return fmtBRL.format(value);
                        }
                    }
                }
            }
        }
    });
}