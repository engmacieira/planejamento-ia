CREATE TABLE public.grupos (
    id SERIAL PRIMARY KEY,
    
    -- Quem é o pai? (O "CC" da árvore)
    id_categoria INTEGER NOT NULL REFERENCES public.categorias(id),
    
    -- Código do Grupo (O "GG")
    codigo CHAR(2) NOT NULL, -- Ex: '01'
    
    nome VARCHAR(150) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    
    -- Constraint: Dentro da categoria 01, só pode haver um grupo 01.
    CONSTRAINT uk_grupo_codigo UNIQUE (id_categoria, codigo)
);

CREATE INDEX idx_grupos_categoria ON public.grupos(id_categoria);