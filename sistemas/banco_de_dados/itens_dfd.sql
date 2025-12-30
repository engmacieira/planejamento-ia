CREATE TABLE public.itens_dfd (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo com o DFD (O Pai)
    id_dfd INTEGER NOT NULL REFERENCES public.dfd(id) ON DELETE CASCADE,
    
    -- O Produto (Vem do Catálogo)
    id_catalogo_item INTEGER NOT NULL REFERENCES public.catalogo_itens(id),

	-- Organização Visual
    numero_item INT NOT NULL,
    
    -- Quantitativos Estimados (Expectativa)
    quantidade NUMERIC(15,3) NOT NULL, 
    valor_unitario_estimado NUMERIC(15,2) NOT NULL, 
    
    -- Total calculado automaticamente (Performance)
    valor_total_estimado NUMERIC(15,2) GENERATED ALWAYS AS (quantidade * valor_unitario_estimado) STORED,
    
    -- Constraint: Não pode pedir o mesmo produto duas vezes no mesmo DFD
    CONSTRAINT uk_item_dfd UNIQUE (id_dfd, id_catalogo_item)
);

-- Índices
CREATE INDEX idx_itens_dfd_doc ON public.itens_dfd(id_dfd);
CREATE INDEX idx_itens_dfd_produto ON public.itens_dfd(id_catalogo_item);