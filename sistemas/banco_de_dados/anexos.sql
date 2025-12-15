CREATE TABLE public.anexos (
    id SERIAL PRIMARY KEY,
    
    -- Metadados do Arquivo
    nome_original VARCHAR(255) NOT NULL, -- O nome que o usuário subiu: "contrato_final.pdf"
    nome_seguro VARCHAR(255) NOT NULL UNIQUE, -- UUID ou Hash gerado pelo sistema para salvar no disco/S3
    caminho_arquivo VARCHAR(500), -- Opcional: Caminho da pasta ou Bucket S3
    tamanho_bytes BIGINT, -- Útil para controle de storage
    mimetype VARCHAR(100), -- Ex: 'application/pdf', 'image/png'
    
    -- Relacionamento Forte (Correção)
    id_tipo_documento INTEGER REFERENCES public.tipos_documento(id), 
    
    -- Vínculos (Polimorfismo Exclusivo)
    id_contrato INTEGER REFERENCES public.contratos(id) ON DELETE CASCADE,
    id_aocs INTEGER REFERENCES public.aocs(id) ON DELETE CASCADE,
    
    -- Auditoria
    data_upload TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraint de Integridade:
    -- Garante que o anexo pertença A UM e APENAS UM registro (Ou é de Contrato, ou é de AOCS)
    -- Isso impede anexo órfão ou duplicado logicamente.
    CONSTRAINT check_origem_anexo CHECK (
        (id_contrato IS NOT NULL AND id_aocs IS NULL) OR
        (id_contrato IS NULL AND id_aocs IS NOT NULL)
    )
);