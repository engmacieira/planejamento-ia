CREATE TABLE public.dotacao (
    id SERIAL PRIMARY KEY,
    
    -- O Campo mais importante: O Ano do Orçamento
    exercicio INT NOT NULL, 
    
    -- O código completo (funcional programática + natureza)
    -- Ex: "02.03.10.301.0001.2001.3.3.90.30.00"
    codigo_dotacao VARCHAR(100) NOT NULL,
    
    -- Campo opcional, mas muito comum em prefeituras ("Ficha 512")
    numero_ficha INT, 
    
    -- Descrição legível para o humano não precisar decorar o código
    -- Ex: "Material de Consumo - Secretaria de Saúde"
    descricao TEXT, 
    
    saldo_inicial NUMERIC(15,2), -- Opcional: Se quiser controlar saldo
    ativo BOOLEAN DEFAULT TRUE,

    -- Constraint: No mesmo ano, não pode haver duas dotações com o mesmo código
    CONSTRAINT uk_dotacao_exercicio_codigo UNIQUE (exercicio, codigo_dotacao)
);

-- Índice: Busca rápida por ano
CREATE INDEX idx_dotacao_exercicio ON public.dotacao(exercicio);