CREATE TABLE public.perfis (
    id SERIAL PRIMARY KEY,
    
    nome VARCHAR(50) NOT NULL UNIQUE, -- Ex: "Administrador", "Pregoeiro", "Fiscal", "Visualizador"
    descricao TEXT, -- Ex: "Acesso total ao sistema"
    
    ativo BOOLEAN DEFAULT TRUE
);

-- Inserção inicial básica (Seed)
INSERT INTO public.perfis (nome, descricao) VALUES 
('Administrador', 'Acesso total ao sistema'),
('Operador', 'Pode cadastrar e editar, mas não pode excluir'),
('Consulta', 'Apenas visualização de relatórios');