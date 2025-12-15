CREATE TABLE public.itens_contrato (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo com o Contrato (O Pai Jurídico)
    id_contrato INTEGER NOT NULL REFERENCES public.contratos(id) ON DELETE CASCADE,
    
    -- Vínculo com a Origem da Demanda (O Elo de Rastreabilidade)
    id_item_dfd INTEGER NOT NULL REFERENCES public.itens_dfd(id),
    
    -- Organização Visual
    numero_item INT NOT NULL, -- Sequencial no contrato (Item 01, Item 02...)
    
    -- Dados Reais (Resultado da Licitação)
    marca VARCHAR(150), -- A marca vencedora (Ex: "Faber Castell")
    
    -- Valores Finais
    quantidade_contratada NUMERIC(15,3) NOT NULL, -- Pode ser igual ou menor que a do DFD
    valor_unitario_final NUMERIC(15,2) NOT NULL,  -- O preço real ganho na licitação
    
    -- Cálculo Automático
    valor_total_item NUMERIC(15,2) GENERATED ALWAYS AS (quantidade_contratada * valor_unitario_final) STORED,
    
    ativo BOOLEAN DEFAULT TRUE,

    -- Constraints
    -- 1. Não pode repetir o mesmo número de item no mesmo contrato
    CONSTRAINT uk_item_numero_contrato UNIQUE (id_contrato, numero_item),
    
    -- 2. Não deve ser possível vincular o MESMO item específico do DFD duas vezes no mesmo contrato
    CONSTRAINT uk_item_origem_duplicada UNIQUE (id_contrato, id_item_dfd)
);

-- Índices
CREATE INDEX idx_itens_contrato_pai ON public.itens_contrato(id_contrato);
CREATE INDEX idx_itens_contrato_origem ON public.itens_contrato(id_item_dfd);