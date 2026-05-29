const API_BASE = "/api/v1";

document.addEventListener("DOMContentLoaded", function () {
    const inputCep = document.getElementById("cep");
    if (inputCep) {
        IMask(inputCep, { mask: "00000-000" });
    }

    const inputGasto = document.getElementById("gasto");
    if (inputGasto) {
        IMask(inputGasto, {
            mask: "R$ num",
            blocks: {
                num: {
                    mask: Number,
                    thousandsSeparator: ".",
                    radix: ",",
                    scale: 2,
                    padFractionalZeros: true,
                },
            },
        });
    }
});

function parseGastoParaNumero(valorFormatado) {
    const limpo = valorFormatado
        .replace(/[^\d,.-]/g, "")
        .replace(/\./g, "")
        .replace(",", ".");
    return parseFloat(limpo);
}

function validarEAbrirModal() {
    const valorCep = document.getElementById("cep").value.trim();
    const valorGasto = document.getElementById("gasto").value.trim();

    if (valorCep === "" || valorGasto === "") {
        alert("Atenção: Por favor, preencha o CEP e o seu Gasto Médio Mensal para gerar a simulação.");
        return;
    }
    if (valorCep.length < 9) {
        alert("Atenção: Por favor, digite um CEP válido com 8 números.");
        return;
    }
    const numero = parseGastoParaNumero(valorGasto);
    if (!numero || numero <= 0) {
        alert("Atenção: Informe um valor de gasto mensal válido.");
        return;
    }

    new bootstrap.Modal(document.getElementById("modalLead")).show();
}

async function enviarSimulacao(event) {
    event.preventDefault();

    const nome = document.getElementById("nome_lead").value.trim();
    const email = document.getElementById("email_lead").value.trim();
    const cep = document.getElementById("cep").value.trim();
    const valor = parseGastoParaNumero(document.getElementById("gasto").value);

    const erroBox = document.getElementById("erroLead");
    const botao = document.getElementById("btnEnviarLead");
    erroBox.classList.add("d-none");
    botao.disabled = true;
    botao.innerText = "Calculando...";

    try {
        const resposta = await fetch(`${API_BASE}/simulacoes/publica`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nome,
                email,
                cep,
                valor_reais: valor,
            }),
        });

        if (!resposta.ok) {
            const detalhe = await resposta.json().catch(() => ({}));
            throw new Error(detalhe.detail || "Falha ao processar simulação.");
        }

        const dados = await resposta.json();
        window.location.href = `/dashboard?id=${dados.simulacao_id}`;
    } catch (err) {
        erroBox.innerText = err.message;
        erroBox.classList.remove("d-none");
        botao.disabled = false;
        botao.innerText = "Enviar";
    }
}
