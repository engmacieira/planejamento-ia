CREATE TABLE public.usuarios (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo de Permissão (RBAC)
    id_perfil INTEGER NOT NULL REFERENCES public.perfis(id),
    
    -- Identificação de Login
    username VARCHAR(50) NOT NULL UNIQUE, -- O "Nick" de acesso (Ex: matheus.dev)
    email VARCHAR(255) NOT NULL UNIQUE,   -- Para recuperação de senha
    password_hash VARCHAR(255) NOT NULL,  -- A senha criptografada (Nunca salvar texto puro!)
    
    -- Dados Pessoais (Identificação Real)
    nome_completo VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE, -- CPF é vital para saber QUEM clicou no botão (responsabilidade jurídica)
    telefone VARCHAR(20),   -- Para 2FA (Autenticação de Dois Fatores) ou contato rápido
    
    -- Auditoria e Segurança
    ativo BOOLEAN DEFAULT TRUE, -- Se o cara for demitido, muda para FALSE (não deleta o registro!)
    ultimo_login TIMESTAMP WITH TIME ZONE, -- Bom para saber se a conta está abandonada
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices de Performance e Segurança
CREATE INDEX idx_usuarios_login ON public.usuarios(username);
CREATE INDEX idx_usuarios_email ON public.usuarios(email);
CREATE INDEX idx_usuarios_cpf ON public.usuarios(cpf);