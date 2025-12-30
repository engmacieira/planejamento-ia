CREATE TABLE public.processos_licitatorios (
    id SERIAL PRIMARY KEY,
    
    -- Vínculo com a Origem (A Demanda)
    -- Garante que todo processo nasça de uma necessidade formalizada
    id_dfd INTEGER NOT NULL REFERENCES public.dfd(id), 
    
    -- Identificação Administrativa (O número da pasta/protocolo)
    -- Ex: "Processo Administrativo nº 520/2023"
    numero_processo INT NOT NULL,
    ano_processo INT NOT NULL,
    
    -- Identificação da Modalidade (O número da disputa)
    -- Trazemos para cá aquela estrutura que discutimos antes.
    -- Ex: "Pregão Eletrônico nº 12/2023"
    id_modalidade INTEGER NOT NULL REFERENCES public.modalidade(id),
    id_numero_modalidade INTEGER REFERENCES public.numeros_modalidade(id), 
    
    -- O Objeto (Resumo do que está sendo licitado)
    objeto TEXT NOT NULL,
    
    -- Valores e Datas
    valor_total_estimado NUMERIC(15,2), -- Soma dos itens do DFD
    data_abertura DATE, -- Quando a sessão pública vai acontecer
    data_homologacao DATE, -- Quando o resultado foi oficializado
    
    -- Controle de Fluxo
    status VARCHAR(50) DEFAULT 'Em Andamento' CHECK (status IN ('Em Andamento', 'Deserto', 'Fracassado', 'Homologado', 'Suspenso', 'Cancelado')),
    
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    -- Não pode haver dois Processos Administrativos com mesmo número/ano
    CONSTRAINT uk_processo_adm UNIQUE (numero_processo, ano_processo),
    -- Um DFD só gera um processo (Regra de 1:1 para simplificar, se for o caso)
    CONSTRAINT uk_processo_dfd UNIQUE (id_dfd)
);

-- Índices
CREATE INDEX idx_proc_numero ON public.processos_licitatorios(numero_processo, ano_processo);
CREATE INDEX idx_proc_modalidade ON public.processos_licitatorios(id_numero_modalidade);