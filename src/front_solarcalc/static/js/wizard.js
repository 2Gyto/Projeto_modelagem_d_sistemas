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

// Intercepta o lead: autenticação fantasma → rascunho da simulação → redirecionamento
document.addEventListener("DOMContentLoaded", function() {
    var formLead = document.getElementById("formLead");
    if (!formLead) {
        return;
    }

    formLead.addEventListener("submit", async function(event) {
        event.preventDefault();

        var nomeUsuario = document.getElementById("nomeLead").value.trim();
        var emailUsuario = document.getElementById("emailLead").value.trim();
        var valorCep = document.getElementById("cep").value;
        var valorGasto = document.getElementById("gasto").value;
        var tipoInstalacao = document.querySelector('input[name="tipo"]:checked').id;

        var btn = this.querySelector('button[type="submit"]');
        var textoOriginal = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Calculando...';
        btn.disabled = true;
        btn.classList.add("disabled");

        try {
            // 1) Register (ignora conflito) + login → token em localStorage
            await autenticarPorEmail(nomeUsuario, emailUsuario);

            // 2) Cria rascunho, executa cálculo (Authorization: Bearer) e persiste ID
            var simulacaoId = await criarEExecutarSimulacao({
                cep: valorCep,
                gasto: valorGasto,
                tipo: tipoInstalacao,
            });

            localStorage.setItem("simulacao_id", simulacaoId);

            // 3) Redireciona somente após token e simulacao_id disponíveis
            var destino = "resultado.html?nome=" + encodeURIComponent(nomeUsuario);
            destino += "&simulacao_id=" + encodeURIComponent(simulacaoId);
            window.location.href = destino;
        } catch (erro) {
            console.error("Erro na integração:", erro);
            alert(erro.message || "Ops! Houve uma falha ao comunicar com o servidor.");
            btn.innerHTML = textoOriginal;
            btn.disabled = false;
            btn.classList.remove("disabled");
        }
    });
});
