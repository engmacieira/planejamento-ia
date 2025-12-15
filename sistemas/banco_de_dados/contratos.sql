CREATE TABLE public.contratos (
    id SERIAL PRIMARY KEY,
    
    -- Identificação do Contrato
    numero_contrato INT NOT NULL,
    ano_contrato INT NOT NULL,
    
    -- Hierarquia: Processo Licitatório
    id_processo_licitatorio INTEGER NOT NULL REFERENCES public.processos_licitatorios(id),
    
    -- A Modalidade Específica (O Ajuste Solicitado)
    -- Aponta para "Pregão 10/2023" e não apenas para "Pregão"
    id_numero_modalidade INTEGER NOT NULL REFERENCES public.numeros_modalidade(id),
    
    -- Quem?
    id_fornecedor INTEGER NOT NULL REFERENCES public.fornecedores(id),
    
    -- Classificação
    id_instrumento_contratual INTEGER REFERENCES public.instrumentocontratual(id), 
    
    -- Vigência
    data_assinatura DATE NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE NOT NULL,
    
    valor_total NUMERIC(15,2) DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_contrato_full UNIQUE (numero_contrato, ano_contrato),
    CONSTRAINT check_vigencia CHECK (data_fim_vigencia >= data_inicio_vigencia)
);