CREATE TABLE public.modalidade (
    id SERIAL PRIMARY KEY,
    
    -- Nome descritivo
    nome VARCHAR(100) NOT NULL UNIQUE, -- Ex: "Pregão Eletrônico", "Dispensa de Licitação"
    
    -- Sigla para uso em códigos de processo
    sigla VARCHAR(10), -- Ex: "PE", "CC", "DL"
    
    -- Referência Legal (Opcional, mas chique para gerar cabeçalhos de documentos)
    fundamentacao_legal VARCHAR(255), -- Ex: "Lei 14.133/2021, Art. 28"
    
    ativo BOOLEAN DEFAULT TRUE, -- Para desativar "Convite" ou "Tomada de Preços" que morreram
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);