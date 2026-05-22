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

// Intercepta o clique de "Enviar" no Modal de Lead
document.getElementById('formLead').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede a página de recarregar
    
    var nomeUsuario = document.getElementById('nomeLead').value;
    
    // Altera o botão para dar um feedback visual legal
    var btn = this.querySelector('button[type="submit"]');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Gerando link...';
    btn.classList.add('disabled');

    // Finge que demorou 1,5 segundos para "enviar o email" e redireciona
    setTimeout(function() {
        // Redireciona para o dashboard passando o nome na URL (Ex: resultado.html?nome=Carlos)
        window.location.href = "resultado.html?nome=" + encodeURIComponent(nomeUsuario);
    }, 1500);
});