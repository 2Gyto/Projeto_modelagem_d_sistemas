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
    
    // 1. Captura os dados do formulário principal e do Pop-up
    var nomeUsuario = document.getElementById('nomeLead').value;
    var valorCep = document.getElementById('cep').value;
    var valorGasto = document.getElementById('gasto').value;
    var tipoInstalacao = document.querySelector('input[name="tipo"]:checked').id;

    // 2. Monta o pacote no formato JSON (a linguagem universal da internet)
    var pacoteDeDados = {
        nome: nomeUsuario,
        cep: valorCep,
        gasto: valorGasto,
        tipo: tipoInstalacao
    };

    // Altera o botão para dar um feedback visual legal
    var btn = this.querySelector('button[type="submit"]');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Calculando...';
    btn.classList.add('disabled');

    // 3. A PONTE: Envia o pacote para o Back-end do Django
    // (O Django do seu colega precisará ter uma rota criada chamada '/api/simular/')
    fetch('http://127.0.0.1:8000/api/v1/simulacoes/teste-integracao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // O Django exige um token de segurança chamado CSRF. 
            // Para testes iniciais, seu colega pode desativar essa exigência na rota dele.
        },
        body: JSON.stringify(pacoteDeDados)
    })
    .then(response => response.json()) // Espera o Django responder com os cálculos
    .then(dadosDoBackEnd => {
        // Quando o Django responder, redirecionamos para o dashboard!
        window.location.href = "resultado.html?nome=" + encodeURIComponent(nomeUsuario);
    })
    .catch(erro => {
        console.error("Erro na integração:", erro);
        alert("Ops! Houve uma falha ao comunicar com o servidor.");
        
        // Volta o botão ao normal em caso de erro
        btn.innerHTML = 'Enviar';
        btn.classList.remove('disabled');
    });
});