CREATE TABLE public.categorias (
    id SERIAL PRIMARY KEY,
    
    -- Identificação Visual
    nome VARCHAR(150) NOT NULL UNIQUE, -- Ex: "Material Médico Hospitalar"
    
    -- Identificação Taxonômica (O "CC" do código CCGGSSIIII)
    codigo_taxonomia CHAR(2) NOT NULL UNIQUE, -- Ex: '01', '02' (Fixo em 2 caracteres)
    
    -- Controle
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para garantir performance se você filtrar pelo código
CREATE INDEX idx_categorias_codigo ON public.categorias(codigo_taxonomia);