CREATE TABLE public.aocs (
    id SERIAL PRIMARY KEY,
    
    -- Identificação do Documento
    numero_aocs VARCHAR(100) NOT NULL UNIQUE, -- O número final gerado
    ano_aocs INT NOT NULL,
    
    -- Referência Externa (Opcional)
    -- Se a secretaria manda um memorando físico nº 500, você anota aqui.
    numero_pedido_externo VARCHAR(50), 
    
    -- Datas
    data_emissao DATE DEFAULT CURRENT_DATE NOT NULL, -- Quando a AOCS foi gerada
    
    -- Atores (Quem pediu e Quem paga)
    id_unidade_requisitante INTEGER NOT NULL REFERENCES public.unidadesrequisitantes(id), -- Secretaria de Saúde
    id_solicitante INTEGER REFERENCES public.agentes_responsaveis(id), -- Funcionário João
    id_agente_responsavel INTEGER REFERENCES public.agentes_responsaveis(id), -- O Gestor que assinou a AOCS
    
    -- Logística e Financeiro
    id_local_entrega INTEGER REFERENCES public.locais_entrega(id),
    id_dotacao INTEGER REFERENCES public.dotacao(id),
    empenho VARCHAR(50), 
    
    -- Controle de Estado
    status VARCHAR(30) DEFAULT 'Emitida' CHECK (status IN ('Rascunho', 'Emitida', 'Entregue Parcial', 'Finalizada', 'Cancelada')),
    justificativa TEXT,
    
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_aocs_numero ON public.aocs(numero_aocs);
CREATE INDEX idx_aocs_requisitante ON public.aocs(id_unidade_requisitante);
CREATE INDEX idx_aocs_empenho ON public.aocs(empenho);