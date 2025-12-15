const API_URL = "http://127.0.0.1:8000";

// --- FUNÇÕES DE AUTH ---

function checkAuth() {
    const token = localStorage.getItem("token");
    if (!token) {
        // Se não tem token, manda pro login (vamos criar a login.html depois)
        // Por enquanto, vamos fazer um login forçado via prompt só pra testar
        const email = prompt("Login necessário! Digite seu email (ex: admin@sistema.com):");
        const password = prompt("Digite sua senha:");
        login(email, password);
    } else {
        // Se tem token, carrega a lista
        loadProcesses();
    }
}

async function login(email, password) {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Login falhou");

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        location.reload(); // Recarrega para entrar
    } catch (error) {
        alert("Erro no login: " + error.message);
    }
}

function logout() {
    localStorage.removeItem("token");
    location.reload();
}

// --- FUNÇÕES DE PROCESSOS ---

async function loadProcesses() {
    const token = localStorage.getItem("token");
    const tbody = document.getElementById("lista-processos");

    try {
        const response = await fetch(`${API_URL}/processos/`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            logout(); // Token expirou
            return;
        }

        const processos = await response.json();
        
        // Limpa a tabela
        tbody.innerHTML = "";

        if (processos.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center py-4">Nenhum processo encontrado.</td></tr>`;
            return;
        }

        // Desenha as linhas
        processos.forEach(proc => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="fw-bold">${proc.numero_dfd}</td>
                <td>${proc.secretaria}</td>
                <td class="text-truncate" style="max-width: 300px;">${proc.objeto}</td>
                <td class="text-end">
                    <button onclick="baixarZip(${proc.id})" class="btn btn-sm btn-primary">
                        ⬇️ Baixar ZIP
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        console.error("Erro:", error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Erro ao carregar dados.</td></tr>`;
    }
}

async function baixarZip(id) {
    const token = localStorage.getItem("token");
    
    // Feedback visual
    const btn = event.target;
    const originalText = btn.innerText;
    btn.innerText = "⏳ Gerando...";
    btn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/processos/${id}/gerar_zip`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Erro ao gerar ZIP");
        }

        // Truque para baixar arquivo (Blob)
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        // Tenta pegar o nome do arquivo do header ou usa um padrão
        a.download = `Processo_${id}.zip`; 
        document.body.appendChild(a);
        a.click();
        a.remove();

    } catch (error) {
        alert("Erro: " + error.message);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function salvarProcesso() {
    const token = localStorage.getItem("token");
    const form = document.getElementById("formProcesso");
    
    // Transforma os dados do formulário em Objeto JSON
    const formData = new FormData(form);
    const dados = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_URL}/processos/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(dados)
        });

        if (!response.ok) {
            const erro = await response.json();
            alert("Erro ao salvar: " + (erro.detail || "Verifique os dados"));
            return;
        }

        alert("✅ Processo salvo com sucesso!");
        
        // Fecha o modal (usando Bootstrap)
        const modalEl = document.getElementById('modalNovoProcesso');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();

        // Limpa o form e recarrega a tabela
        form.reset();
        loadProcesses();

    } catch (error) {
        console.error(error);
        alert("Erro de conexão ao salvar.");
    }
}

// Inicia
checkAuth();