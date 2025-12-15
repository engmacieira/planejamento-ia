CREATE TABLE public.subgrupos (
    id SERIAL PRIMARY KEY,
    
    -- Quem é o pai? (O "GG" da árvore)
    id_grupo INTEGER NOT NULL REFERENCES public.grupos(id),
    
    -- Código do Subgrupo (O "SS")
    codigo CHAR(2) NOT NULL, -- Ex: '01'
    
    nome VARCHAR(150) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    
    -- Constraint: Dentro do grupo X, só pode haver um subgrupo Y.
    CONSTRAINT uk_subgrupo_codigo UNIQUE (id_grupo, codigo)
);

CREATE INDEX idx_subgrupos_grupo ON public.subgrupos(id_grupo);