SELECT 
    p.nome_postos AS 'Posto',
    p.endereco AS 'Endereço',
    p.bairro AS 'Bairro',
    p.cidade AS 'Cidade',
    p.estado AS 'Estado',
    c.tipo_combustivel AS 'Tipo de Combustível',
    co.preco AS 'Preço',
    co.data_coleta AS 'Data da Coleta',
    AVG(co.preco) OVER () AS 'Preço Médio Geral',  -- Preço médio geral
    AVG(co.preco) OVER (PARTITION BY p.bairro) AS 'Preço Médio por Bairro'  -- Preço médio por bairro
FROM 
    coleta co
JOIN 
    postos p ON co.postos_idpostos = p.idpostos
JOIN 
    combustivel c ON co.combustivel_idcombustivel = c.idcombustivel
WHERE 
    (co.data_coleta BETWEEN '2025-02-01' AND '2025-02-28' OR '2025-02-28' IS NULL)  -- Filtro opcional de data
    AND (p.bairro = 'Santa Inês' OR 'Santa Inês' IS NULL)  -- Filtro opcional de bairro
ORDER BY 
    p.nome_postos, c.tipo_combustivel;
    
SELECT 
    p.nome_postos AS 'Posto',
    p.endereco AS 'Endereço',
    p.bairro AS 'Bairro',
    p.cidade AS 'Cidade',
    p.estado AS 'Estado',
    c.tipo_combustivel AS 'Tipo de Combustível',
    co.preco AS 'Preço',
    co.data_coleta AS 'Data da Coleta',
    AVG(co.preco) OVER () AS 'Preço Médio Geral',  -- Preço médio geral
    AVG(co.preco) OVER (PARTITION BY p.bairro) AS 'Preço Médio por Bairro'  -- Preço médio por bairro
FROM 
    coleta co
JOIN 
    postos p ON co.postos_idpostos = p.idpostos
JOIN 
    combustivel c ON co.combustivel_idcombustivel = c.idcombustivel
WHERE 
    (co.data_coleta BETWEEN '2025-02-01' AND '2025-02-28' OR '2025-02-28' IS NULL)  -- Filtro opcional de data
    AND (p.bairro = 'Santa Inês' OR 'Santa Inês' IS NULL)  -- Filtro opcional de bairro
ORDER BY 
    p.nome_postos, c.tipo_combustivel
INTO OUTFILE '/path/to/your/file.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';coletacoleta
