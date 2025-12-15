CREATE TABLE public.dfd (
    id SERIAL PRIMARY KEY,
    
    -- Identificação (Numero/Ano separados, igual você pediu)
    numero INT NOT NULL,
    ano INT NOT NULL,
    
    descricao_sucinta VARCHAR(255) NOT NULL, -- Ex: "Aquisição de Material de Escritório"
    justificativa_necessidade TEXT,
    
    -- Quem está pedindo?
    id_unidade_requisitante INTEGER NOT NULL REFERENCES public.unidadesrequisitantes(id),
    
    data_criacao DATE DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'Rascunho', -- Rascunho, Em Aprovação, Aprovado, Vinculado a Processo
    
    -- Garante que não exista dois DFD nº 01/2024
    CONSTRAINT uk_dfd_numero_ano UNIQUE (numero, ano)
);