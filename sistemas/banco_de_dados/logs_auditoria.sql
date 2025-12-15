CREATE TABLE public.logs_auditoria (
    id SERIAL PRIMARY KEY,
    
    -- Quem fez?
    id_usuario INTEGER REFERENCES public.usuarios(id) ON DELETE SET NULL,
    username_snapshot VARCHAR(80), -- Gravamos o nome também, pois se o usuário for deletado, ainda sabemos quem foi
    
    -- Quando e Onde?
    data_acao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_origem VARCHAR(45), -- IPv4 ou IPv6
    
    -- O que foi afetado?
    tabela_afetada VARCHAR(100) NOT NULL, -- Ex: 'contratos'
    id_registro_afetado INTEGER, -- O ID da linha que foi mexida (Ex: ID do contrato)
    tipo_acao VARCHAR(20) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE', 'LOGIN'
    
    -- O Pulo do Gato: O que mudou?
    -- Usamos JSONB para guardar flexibilidade. 
    -- Ex: {"valor": 100} -> {"valor": 200}
    dados_antigos JSONB, 
    dados_novos JSONB,   
    
    descricao_legivel TEXT -- Uma frase resumo: "Alterou valor do contrato X"
);

-- Índices para Auditoria Rápida
-- "Quem mexeu no contrato 50?"
CREATE INDEX idx_logs_entidade ON public.logs_auditoria(tabela_afetada, id_registro_afetado);
-- "O que o usuário X fez hoje?"
CREATE INDEX idx_logs_usuario ON public.logs_auditoria(id_usuario, data_acao);
-- "Performance no JSON" (Opcional, se precisar buscar DENTRO do json)
CREATE INDEX idx_logs_novos ON public.logs_auditoria USING gin(dados_novos);