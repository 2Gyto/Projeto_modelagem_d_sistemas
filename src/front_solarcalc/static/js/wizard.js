// Aguarda a página carregar por completo para aplicar as máscaras
document.addEventListener("DOMContentLoaded", function() {
    
    // Máscara do CEP
    var inputCep = document.getElementById('cep');
    if (inputCep) {
        IMask(inputCep, { mask: '00000-000' });
    }

    // Máscara de Reais (Gasto)
    var inputGasto = document.getElementById('gasto');
    if (inputGasto) {
        IMask(inputGasto, {
            mask: 'R$ num',
            blocks: {
                num: {
                    mask: Number,
                    thousandsSeparator: '.',
                    radix: ',',
                    scale: 2,
                    padFractionalZeros: true
                }
            }
        });
    }
});

// Função acionada pelo botão "Simular"
function validarEAbrirModal() {
    var campoCep = document.getElementById('cep');
    var campoGasto = document.getElementById('gasto');

    var valorCep = campoCep.value.trim();
    var valorGasto = campoGasto.value.trim();

    // 1. Bloqueia se estiver vazio
    if (valorCep === "" || valorGasto === "") {
        alert("Atenção: Por favor, preencha o CEP e o seu Gasto Médio Mensal para gerar a simulação.");
        return; // Interrompe a função, o modal não abre
    }

    // 2. Bloqueia se o CEP estiver incompleto
    if (valorCep.length < 9) {
        alert("Atenção: Por favor, digite um CEP válido com 8 números.");
        return; 
    }

    // 3. Se tudo estiver preenchido e correto, abre o Pop-up do Bootstrap via JavaScript
    var meuModal = new bootstrap.Modal(document.getElementById('modalLead'));
    meuModal.show();
}