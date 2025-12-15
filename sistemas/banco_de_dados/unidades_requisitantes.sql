CREATE TABLE public.unidades_requisitantes (
    id SERIAL PRIMARY KEY,
    
    -- Identificação Visual
    nome VARCHAR(255) NOT NULL UNIQUE, -- Ex: "Secretaria Municipal de Saúde"
    sigla VARCHAR(20), -- Ex: "SMS", "SEMED" (Ótimo para relatórios compactos)
    
    -- Identificação Administrativa
    codigo_administrativo VARCHAR(20), -- Ex: "02.01" (Código do Organograma/Contabilidade)
    
    -- Hierarquia (O Pulo do Gato)
    -- Permite saber que o "Almoxarifado Central" pertence à "Administração"
    id_unidade_pai INTEGER REFERENCES public.unidades_requisitantes(id),
    
    -- Controle
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_unidades_nome ON public.unidades_requisitantes(nome);
CREATE INDEX idx_unidades_pai ON public.unidades_requisitantes(id_unidade_pai); -- Acelera buscar "Quem são os filhos da Secretaria X?"