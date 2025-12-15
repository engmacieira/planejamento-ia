CREATE TABLE public.catalogo_itens (
    id SERIAL PRIMARY KEY,
    
    -- Quem é o pai? (O "SS" da árvore)
    id_subgrupo INTEGER NOT NULL REFERENCES public.subgrupos(id),
    
    -- Dados Básicos
    nome_item VARCHAR(255) NOT NULL,
    unidade_medida VARCHAR(50) NOT NULL, -- UN, CX, FR, KG
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Consumo', 'Permanente', 'Serviço')),
    
    -- Códigos Externos (Governo)
    codigo_catmat_catser VARCHAR(50), -- Opcional
    
    -- Nossa Taxonomia Interna
    numero_sequencial_taxonomia CHAR(4) NOT NULL, -- O "IIII" (Ex: '0001')
    
    -- O Código Completo para busca (CCGGSSIIII)
    -- Deve ser preenchido pela aplicação concatenando Categoria+Grupo+Subgrupo+Sequencial
    codigo_identificacao_completo VARCHAR(10) UNIQUE, 
    
    descricao_detalhada TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Garante que não repita o número 0001 dentro do mesmo subgrupo
    CONSTRAINT uk_item_sequencial UNIQUE (id_subgrupo, numero_sequencial_taxonomia)
);

-- Índices de Performance
-- Busca textual rápida no nome do item
CREATE INDEX idx_catalogo_nome ON public.catalogo_itens USING gin(to_tsvector('portuguese', nome_item));
-- Busca pelo código inteligente "0101010001"
CREATE INDEX idx_catalogo_codigo_full ON public.catalogo_itens(codigo_identificacao_completo);