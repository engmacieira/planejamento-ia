CREATE TABLE public.ci_pagamentos (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo Principal (A "mãe" do pagamento)
    id_aocs INTEGER NOT NULL REFERENCES public.aocs(id),
    
    -- Identificação
    numero_ci VARCHAR(50) NOT NULL UNIQUE,
    data_ci DATE NOT NULL,
    
    -- Quem operou o pagamento? (Diferente de quem pediu a AOCS)
    id_solicitante INTEGER REFERENCES public.agentes_responsaveis(id), 
    
    -- Fonte de Recurso Real (Pode diferir da prevista na AOCS)
    id_dotacao_pagamento INTEGER REFERENCES public.dotacao(id),
    
    -- Dados da Nota Fiscal
    numero_nota_fiscal VARCHAR(100) NOT NULL,
    serie_nota_fiscal VARCHAR(50),
    data_nota_fiscal DATE NOT NULL,
    valor_nota_fiscal NUMERIC(15,2) NOT NULL CHECK (valor_nota_fiscal >= 0),
    codigo_acesso_nota VARCHAR(44), 
    
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);