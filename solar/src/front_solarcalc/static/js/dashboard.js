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
