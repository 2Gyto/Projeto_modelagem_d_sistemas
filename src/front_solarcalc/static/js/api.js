const API_BASE = window.SOLARCALC_API || "http://127.0.0.1:8000/api/v1";

function getToken() {
    return localStorage.getItem("solarcalc_token");
}

function setToken(token) {
    localStorage.setItem("solarcalc_token", token);
}

function clearToken() {
    localStorage.removeItem("solarcalc_token");
    localStorage.removeItem("solarcalc_simulacao_id");
    localStorage.removeItem("solarcalc_usuario_nome");
}

async function apiFetch(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    const token = getToken();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        let msg = data.detail || data.message || "Erro na requisição.";
        if (Array.isArray(msg)) {
            msg = msg.map((d) => (typeof d === "string" ? d : d.msg || JSON.stringify(d))).join(" ");
        }
        const err = new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
        err.status = response.status;
        err.api = data.api;
        throw err;
    }
    return data;
}

async function registrar(nome, email, senha) {
    return apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ nome, email, senha }),
    });
}

async function login(email, senha) {
    const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, senha }),
    });
    setToken(data.access_token);
    return data;
}

async function simularCompleto(payload) {
    const data = await apiFetch("/simulacoes/completa", {
        method: "POST",
        body: JSON.stringify(payload),
    });
    localStorage.setItem("solarcalc_simulacao_id", data.id);
    return data;
}

async function obterSimulacao(id) {
    return apiFetch(`/simulacoes/${id}`);
}

function formatarMoeda(valor) {
    const n = Number(valor);
    return n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}
