CREATE TABLE public.locais_entrega (
    id SERIAL PRIMARY KEY,
    
    -- Identificação do Local (Nome conhecido)
    nome VARCHAR(200) NOT NULL UNIQUE, -- Ex: "Almoxarifado Central", "UBS Vila Nova"
    
    -- Endereço Físico (Estruturado para Logística/Correios/NF-e)
    logradouro VARCHAR(255) NOT NULL, -- Rua, Avenida...
    numero VARCHAR(20) NOT NULL,      -- "123", "S/N"
    complemento VARCHAR(100),         -- "Bloco B", "Fundos"
    bairro VARCHAR(100) NOT NULL,
    cep VARCHAR(10),                  -- Ex: "12345-678"
    
    -- Contato no Local (Opcional, mas útil)
    telefone_contato VARCHAR(20),     -- Ex: Recepção do local
    
    -- Controle
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice (Geralmente buscamos pelo nome do local)
CREATE INDEX idx_locais_nome ON public.locais_entrega(nome);