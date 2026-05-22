/**
 * NÚCLEO DO PROJETO: CONTRATO DE DADOS
 * Todo o grupo deve se basear nesta estrutura.
 */
function processarSimulacao(cep, gastoMensal, tipoInstalacao) {
    
    // 1. DADOS IMAGINÁRIOS (Aqui entrarão as APIs e o Django no futuro)
    // Usando R$ 0.830 como exemplo da tarifa média local
    const dadosFalsos = {
        investimento_total: "R$ 15.000",
        payback_texto: "3 anos e 4 meses",
        economia_mensal: "R$ 320,00",
        lucro_25_anos: "R$ 110.000",
        
        // Dados imaginários para o Gráfico (Chart.js) desenhar as linhas
        grafico_anos: [0, 1, 2, 3, 4, 5],
        grafico_linha_concessionaria: [0, 4800, 10080, 15873, 22260, 29280],
        grafico_linha_solar: [15000, 15500, 16000, 16500, 17000]
    };

    // 2. RETORNA O PACOTE
    return dadosFalsos;
}

// static/js/motor_simulacao.js

function obterDadosSimulacao() {
    return {
        // Dados Financeiros (Para os Cards)
        resumo: {
            investimento: "R$ 14.500,00",
            payback: "3 anos e 6 meses",
            economia_mensal: "R$ 310,00",
            lucro_25_anos: "R$ 105.000,00"
        },
        // Dados Técnicos (Para informar o tamanho da obra)
        tecnico: {
            potencia: "3.5 kWp",
            qtd_paineis: "7 a 8 painéis",
            area_telhado: "~ 18 m²",
            marcas: "Canadian, Jinko ou Longi"
        },
        // Dados para o Chart.js (Cruzamento de Linhas)
        grafico: {
            anos_labels: [0, 1, 2, 3, 4, 5],
            linha_concessionaria: [0, 4200, 8800, 13800, 19200, 25000],
            linha_solar: [14500, 15000, 15500, 16000, 16500, 17000]
        }
    };
}