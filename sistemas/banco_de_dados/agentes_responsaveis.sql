CREATE TABLE public.agentes_responsaveis (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE, -- Armazenar apenas dígitos (sem pontos/traços)
    email VARCHAR(255),
    telefone VARCHAR(20),            -- Ex: (11) 91234-5678
    cargo VARCHAR(100),              -- Opcional, mas útil para contexto
    ativo BOOLEAN NOT NULL DEFAULT TRUE, -- Soft Delete
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
-- Índices
CREATE INDEX idx_agentes_nome ON public.agentes_responsaveis(nome);
CREATE INDEX idx_agentes_cpf ON public.agentes_responsaveis(cpf);