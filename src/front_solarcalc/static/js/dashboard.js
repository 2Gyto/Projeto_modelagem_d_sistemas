// static/js/dashboard.js

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Pega o Nome da URL (Ex: ?nome=João)
    const urlParams = new URLSearchParams(window.location.search);
    const nome = urlParams.get('nome');
    if (nome) {
        document.getElementById('nomeUsuario').textContent = nome;
    }

    // 2. Chama o nosso NÚCLEO de dados falsos
    const dados = obterDadosSimulacao();

    // 3. Preenche os Cards
    document.getElementById('txt-investimento').textContent = dados.resumo.investimento;
    document.getElementById('txt-payback').textContent = dados.resumo.payback;
    document.getElementById('txt-economia').textContent = dados.resumo.economia_mensal;
    document.getElementById('txt-lucro').textContent = dados.resumo.lucro_25_anos;

    // 4. Preenche os Dados Técnicos
    document.getElementById('txt-potencia').textContent = dados.tecnico.potencia;
    document.getElementById('txt-paineis').textContent = dados.tecnico.qtd_paineis;
    document.getElementById('txt-area').textContent = dados.tecnico.area_telhado;
    document.getElementById('txt-marcas').textContent = dados.tecnico.marcas;

    // 5. Desenha o Gráfico de Payback
    const ctx = document.getElementById('graficoPayback').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dados.grafico.anos_labels,
            datasets: [
                {
                    label: 'Custo sem Energia Solar (Conta de Luz)',
                    data: dados.grafico.linha_concessionaria,
                    borderColor: '#dc3545', // Vermelho
                    borderDash: [5, 5], // Linha tracejada
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Custo Acumulado com Solar',
                    data: dados.grafico.linha_solar,
                    borderColor: '#FF6B00', // Laranja SolarCalc
                    backgroundColor: 'rgba(255, 107, 0, 0.1)',
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: { callbacks: { label: function(context) { return 'R$ ' + context.parsed.y; } } }
            }
        }
    });
});