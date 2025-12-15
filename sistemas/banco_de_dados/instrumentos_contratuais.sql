CREATE TABLE public.instrumentos_contratuais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE, -- Ex: "Contrato", "Ata de Registro de Preços", "Carta Contrato"
    ativo BOOLEAN DEFAULT TRUE,        -- Para inativar tipos que caiam em desuso
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);