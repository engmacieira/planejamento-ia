CREATE OR REPLACE VIEW v_saldo_itens_contrato AS
SELECT 
    ic.id AS id_item_contrato,
    ic.id_contrato,
    
    -- Trazendo o nome do item (através do DFD -> Catálogo) para facilitar a leitura
    cat.nome_item,
    
    -- Coluna 1: O Teto (Quanto compramos)
    ic.quantidade_contratada,
    
    -- Coluna 2: O Consumo (Soma das AOCS)
    -- Usamos COALESCE para retornar 0 se não houver nenhuma AOCS ainda.
    -- Usamos FILTER para ignorar AOCS canceladas ou itens cancelados.
    COALESCE(SUM(ia.quantidade_solicitada) FILTER (
        WHERE a.status != 'Cancelada' AND ia.status_item != 'Cancelado'
    ), 0) AS total_consumido,
    
    -- Coluna 3: O Saldo Real (A conta de subtração)
    (ic.quantidade_contratada - COALESCE(SUM(ia.quantidade_solicitada) FILTER (
        WHERE a.status != 'Cancelada' AND ia.status_item != 'Cancelado'
    ), 0)) AS saldo_disponivel

FROM itens_contrato ic
-- JOINs para pegar o nome do item (Caminho: Contrato -> DFD -> Catálogo)
JOIN itens_dfd idfd ON ic.id_item_dfd = idfd.id
JOIN catalogo_itens cat ON idfd.id_catalogo_item = cat.id

-- LEFT JOIN com as movimentações (itens_aocs)
-- Usamos LEFT JOIN porque queremos ver o item do contrato mesmo que ele nunca tenha sido usado
LEFT JOIN itens_aocs ia ON ic.id = ia.id_item_contrato
LEFT JOIN aocs a ON ia.id_aocs = a.id

GROUP BY ic.id, ic.id_contrato, cat.nome_item, ic.quantidade_contratada;