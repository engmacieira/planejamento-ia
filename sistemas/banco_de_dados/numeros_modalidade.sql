CREATE TABLE public.numeros_modalidade (
    id SERIAL PRIMARY KEY,
    
    -- O Tipo (Vem da tabela básica: Pregão, Concorrência, etc)
    id_modalidade INTEGER NOT NULL REFERENCES public.modalidade(id),
    
    -- A Numeração Específica
    numero INT NOT NULL,
    ano INT NOT NULL,
    
    -- Auditoria
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Garante que não exista dois "Pregão 10/2023" duplicados
    CONSTRAINT uk_modalidade_numero_ano UNIQUE (id_modalidade, numero, ano)
);

-- Índice para busca rápida (Ex: "Achar o ID do Pregão 10/2023")
CREATE INDEX idx_num_mod_busca ON public.numeros_modalidade(id_modalidade, numero, ano);