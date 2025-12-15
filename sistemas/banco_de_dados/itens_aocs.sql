CREATE TABLE public.itens_aocs (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo Pai (Agora aponta direto para a AOCS)
    id_aocs INTEGER NOT NULL REFERENCES public.aocs(id) ON DELETE CASCADE,
    
    -- Origem do Item (De qual contrato estamos tirando?)
    id_item_contrato INTEGER NOT NULL REFERENCES public.itens_contrato(id),
    
    -- A Movimentação
    quantidade_solicitada NUMERIC(15,3) NOT NULL CHECK (quantidade_solicitada > 0),
    
    -- Auditoria de Saldo (Snapshot)
    -- Como discutimos: gravamos quanto tinha de saldo no momento exato dessa AOCS
    saldo_anterior_snapshot NUMERIC(15,3), 
    
    -- Controle de Entrega
    -- A AOCS pede 100, mas o fornecedor pode entregar em 2x de 50.
    quantidade_entregue NUMERIC(15,3) DEFAULT 0,
    status_item VARCHAR(30) DEFAULT 'Aguardando Entrega' CHECK (status_item IN ('Aguardando Entrega', 'Entregue Total', 'Entregue Parcial', 'Cancelado')),

    -- Integridade:
    -- Não permite duplicar o mesmo item do contrato na mesma AOCS (agrupa-se a quantidade)
    CONSTRAINT uk_aocs_item UNIQUE (id_aocs, id_item_contrato)
);

-- Índices
CREATE INDEX idx_itens_aocs_pai ON public.itens_aocs(id_aocs);
CREATE INDEX idx_itens_aocs_contrato ON public.itens_aocs(id_item_contrato); -- Vital para somar o total consumido do contrato