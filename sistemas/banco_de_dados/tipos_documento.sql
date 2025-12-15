CREATE TABLE public.tipos_documento (
    id SERIAL PRIMARY KEY,
    
    -- O nome do tipo de arquivo
    -- Ex: "Edital", "Nota Fiscal", "Certidão Negativa", "Minuta Contratual"
    nome VARCHAR(100) NOT NULL UNIQUE, 
    
    -- Descrição para orientar o usuário (Opcional)
    -- Ex: "Documento oficial contendo as regras da licitação"
    descricao TEXT, 
    
    -- Controle (Soft Delete)
    ativo BOOLEAN DEFAULT TRUE,
    
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para ordenação alfabética rápida nos dropdowns do sistema
CREATE INDEX idx_tipos_doc_nome ON public.tipos_documento(nome);