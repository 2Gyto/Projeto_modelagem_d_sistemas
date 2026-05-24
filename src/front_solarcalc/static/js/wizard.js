let etapaAtual = 1;
const TOTAL_ETAPAS = 5;
let maskReais = null;
let modalAuth = null;
let pendenteSimulacao = false;

document.addEventListener("DOMContentLoaded", function () {
    modalAuth = new bootstrap.Modal(document.getElementById("modalAuth"));

    const inputReais = document.getElementById("valorReais");
    if (inputReais && window.IMask) {
        maskReais = IMask(inputReais, {
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

    const inputCep = document.getElementById("cep");
    if (inputCep && window.IMask) {
        IMask(inputCep, { mask: "00000-000" });
    }

    document.querySelectorAll('input[name="tipoEntrada"]').forEach((el) => {
        el.addEventListener("change", alternarTipoEntrada);
    });

    document.getElementById("btnAvancar").addEventListener("click", avancar);
    document.getElementById("btnVoltar").addEventListener("click", voltar);
    document.getElementById("btnAuth").addEventListener("click", () => modalAuth.show());
    document.getElementById("formLogin").addEventListener("submit", onLogin);
    document.getElementById("formCadastro").addEventListener("submit", onCadastro);

    atualizarUiAuth();
    mostrarEtapa(1);
});

function alternarTipoEntrada() {
    const tipo = document.querySelector('input[name="tipoEntrada"]:checked').value;
    document.getElementById("campoReais").classList.toggle("d-none", tipo !== "REAIS");
    document.getElementById("campoKwh").classList.toggle("d-none", tipo !== "KWH");
}

function mostrarEtapa(n) {
    etapaAtual = n;
    document.querySelectorAll(".etapa").forEach((el) => {
        el.classList.toggle("d-none", Number(el.dataset.etapa) !== n);
    });
    document.getElementById("etapaBadge").textContent = `Etapa ${n} de ${TOTAL_ETAPAS}`;
    document.getElementById("barraProgresso").style.width = `${(n / TOTAL_ETAPAS) * 100}%`;
    document.getElementById("btnVoltar").disabled = n === 1;
    document.getElementById("btnAvancar").textContent =
        n === TOTAL_ETAPAS ? "Simular agora" : "Avançar";
}

function mostrarErro(msg) {
    const el = document.getElementById("msgErro");
    el.textContent = msg;
    el.classList.remove("d-none");
}

function limparErro() {
    document.getElementById("msgErro").classList.add("d-none");
}

function parseReais(str) {
    if (!str) return 0;
    const limpo = str.replace(/[^\d,]/g, "").replace(",", ".");
    return parseFloat(limpo) || 0;
}

function validarEtapa(n) {
    limparErro();
    if (n === 1) {
        const tipo = document.querySelector('input[name="tipoEntrada"]:checked').value;
        if (tipo === "REAIS") {
            const v = maskReais ? maskReais.unmaskedValue : parseReais(document.getElementById("valorReais").value);
            if (!v || Number(v) <= 0) {
                mostrarErro("Informe um valor em reais maior que zero.");
                return false;
            }
        } else {
            const kwh = Number(document.getElementById("consumoKwh").value);
            if (!kwh || kwh <= 0) {
                mostrarErro("Informe o consumo em kWh maior que zero.");
                return false;
            }
        }
    }
    if (n === 2) {
        const cep = document.getElementById("cep").value.replace(/\D/g, "");
        if (cep.length !== 8) {
            mostrarErro("Informe um CEP válido com 8 dígitos.");
            return false;
        }
    }
    if (n === 3) {
        const area = Number(document.getElementById("areaM2").value);
        if (!area || area < 5) {
            mostrarErro("Informe a área disponível (mínimo 5 m²).");
            return false;
        }
    }
    return true;
}

function montarPayload() {
    const tipo = document.querySelector('input[name="tipoEntrada"]:checked').value;
    const cep = document.getElementById("cep").value;
    const payload = {
        tipo_entrada: tipo,
        cep,
        area_m2: Number(document.getElementById("areaM2").value),
        orientacao: document.getElementById("orientacao").value,
        tipo_conexao: document.getElementById("tipoConexao").value,
    };
    if (tipo === "REAIS") {
        const v = maskReais ? maskReais.unmaskedValue : parseReais(document.getElementById("valorReais").value);
        payload.valor_reais = Number(v);
    } else {
        payload.consumo_kwh = Number(document.getElementById("consumoKwh").value);
    }
    return payload;
}

async function executarSimulacao() {
    const btn = document.getElementById("btnAvancar");
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Consultando APIs...';
    limparErro();

    try {
        const resultado = await simularCompleto(montarPayload());
        sessionStorage.setItem("solarcalc_resultado", JSON.stringify(resultado));
        localStorage.setItem("solarcalc_simulacao_id", resultado.id);
        window.location.href = `resultado.html?id=${resultado.id}`;
    } catch (err) {
        let msg = err.message || "Falha na simulação.";
        if (err.status === 503 && err.api) {
            msg = `${err.message} (${err.api})`;
        }
        mostrarErro(msg);
        btn.disabled = false;
        btn.textContent = "Simular agora";
    }
}

function avancar() {
    if (!validarEtapa(etapaAtual)) return;

    if (etapaAtual < TOTAL_ETAPAS) {
        mostrarEtapa(etapaAtual + 1);
        return;
    }

    if (!getToken()) {
        pendenteSimulacao = true;
        modalAuth.show();
        return;
    }
    executarSimulacao();
}

function voltar() {
    if (etapaAtual > 1) mostrarEtapa(etapaAtual - 1);
}

function atualizarUiAuth() {
    const token = getToken();
    const btn = document.getElementById("btnAuth");
    const label = document.getElementById("usuarioLogado");
    if (token) {
        btn.textContent = "Sair";
        btn.onclick = () => {
            clearToken();
            atualizarUiAuth();
        };
        label.textContent = localStorage.getItem("solarcalc_usuario_nome") || "Conectado";
    } else {
        btn.textContent = "Entrar";
        btn.onclick = () => modalAuth.show();
        label.textContent = "";
    }
}

async function onLogin(e) {
    e.preventDefault();
    const authErro = document.getElementById("authErro");
    authErro.classList.add("d-none");
    try {
        await login(
            document.getElementById("loginEmail").value,
            document.getElementById("loginSenha").value
        );
        localStorage.setItem(
            "solarcalc_usuario_nome",
            document.getElementById("loginEmail").value.split("@")[0]
        );
        modalAuth.hide();
        atualizarUiAuth();
        if (pendenteSimulacao) {
            pendenteSimulacao = false;
            executarSimulacao();
        }
    } catch (err) {
        authErro.textContent = err.message;
        authErro.classList.remove("d-none");
    }
}

async function onCadastro(e) {
    e.preventDefault();
    const authErro = document.getElementById("authErro");
    authErro.classList.add("d-none");
    const nome = document.getElementById("cadNome").value;
    const email = document.getElementById("cadEmail").value;
    const senha = document.getElementById("cadSenha").value;
    try {
        await registrar(nome, email, senha);
        await login(email, senha);
        localStorage.setItem("solarcalc_usuario_nome", nome);
        modalAuth.hide();
        atualizarUiAuth();
        if (pendenteSimulacao) {
            pendenteSimulacao = false;
            executarSimulacao();
        }
    } catch (err) {
        authErro.textContent = err.message;
        authErro.classList.remove("d-none");
    }
}
