document.addEventListener("DOMContentLoaded", async function () {
    const nome = localStorage.getItem("solarcalc_usuario_nome") || "Visitante";
    document.getElementById("nomeUsuario").textContent = nome;

    const simId = new URLSearchParams(window.location.search).get("id")
        || localStorage.getItem("solarcalc_simulacao_id");

    let dados = null;
    const cached = sessionStorage.getItem("solarcalc_resultado");
    if (cached) {
        dados = JSON.parse(cached);
        sessionStorage.removeItem("solarcalc_resultado");
    } else if (simId && typeof obterSimulacao === "function") {
        try {
            dados = await obterSimulacao(simId);
        } catch (e) {
            console.error(e);
            alert("Não foi possível carregar o resultado. Faça uma nova simulação.");
            window.location.href = "index.html";
            return;
        }
    }

    if (!dados || !dados.resultado) {
        alert("Resultado indisponível. Realize uma simulação.");
        window.location.href = "index.html";
        return;
    }

    const r = dados.resultado;
    const loc = dados.localizacao || {};

    document.getElementById("txt-investimento").textContent = formatarMoeda(r.investimento);
    document.getElementById("txt-payback").textContent = r.payback_texto;
    document.getElementById("txt-economia").textContent = formatarMoeda(r.economia_mensal);
    document.getElementById("txt-lucro").textContent = formatarMoeda(r.lucro_25_anos);

    document.getElementById("txt-potencia").textContent =
        r.potencia_kwp ? `${Number(r.potencia_kwp).toFixed(1)} kWp` : "--";
    document.getElementById("txt-paineis").textContent =
        r.qtd_paineis ? `${r.qtd_paineis} painéis` : "--";
    const tel = dados.telhado;
    document.getElementById("txt-area").textContent = tel
        ? `${Number(tel.area_m2).toFixed(0)} m² — ${tel.orientacao}`
        : "--";
    const elHsp = document.getElementById("txt-hsp");
    if (elHsp && loc.hsp_medio_dia) {
        elHsp.textContent = `${Number(loc.hsp_medio_dia).toFixed(2)} h/dia (${loc.cidade || ""}, ${loc.uf || ""})`;
    }
    document.getElementById("txt-marcas").textContent = r.marcas || "--";

    const proj = r.projecoes || [];
    const labels = proj.map((p) => p.ano);
    const linhaConc = proj.map((p) => Number(p.custo_concessionaria));
    const linhaSolar = proj.map((p) => Number(p.custo_fotovoltaico));

    const ctx = document.getElementById("graficoPayback").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Custo acumulado — concessionária (tracejado)",
                    data: linhaConc,
                    borderColor: "#c0392b",
                    borderDash: [8, 4],
                    borderWidth: 2,
                    fill: false,
                    tension: 0.15,
                    pointStyle: "rectRot",
                },
                {
                    label: "Custo acumulado — energia solar",
                    data: linhaSolar,
                    borderColor: "#FF6B00",
                    backgroundColor: "rgba(255, 107, 0, 0.12)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.15,
                    pointStyle: "circle",
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { usePointStyle: true } },
                tooltip: {
                    callbacks: {
                        label: (ctx) =>
                            `${ctx.dataset.label}: ${formatarMoeda(ctx.parsed.y)}`,
                    },
                },
                annotation: r.ano_payback
                    ? undefined
                    : undefined,
            },
            scales: {
                y: {
                    ticks: {
                        callback: (v) =>
                            v.toLocaleString("pt-BR", {
                                style: "currency",
                                currency: "BRL",
                                maximumFractionDigits: 0,
                            }),
                    },
                },
            },
        },
    });
});
