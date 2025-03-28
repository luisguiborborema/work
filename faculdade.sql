-- Criar banco de dados
CREATE SCHEMA IF NOT EXISTS db_postos_vv DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE db_postos_vv;

-- Criar tabela postos
CREATE TABLE IF NOT EXISTS postos (
  idpostos INT NOT NULL AUTO_INCREMENT,
  nome_postos VARCHAR(100) NOT NULL,
  bandeira VARCHAR(50) NULL DEFAULT NULL,
  endereco VARCHAR(255) NOT NULL,
  bairro VARCHAR(100) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  estado VARCHAR(2) NOT NULL,
  telefone VARCHAR(20) NULL DEFAULT NULL,
  atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idpostos)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criar tabela combustivel
CREATE TABLE IF NOT EXISTS combustivel (
  idcombustivel INT NOT NULL AUTO_INCREMENT,
  tipo_combustivel VARCHAR(100) NOT NULL,
  atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idcombustivel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criar tabela coleta
CREATE TABLE IF NOT EXISTS coleta (
  idcoleta INT NOT NULL AUTO_INCREMENT,
  postos_idpostos INT NOT NULL,
  combustivel_idcombustivel INT NOT NULL,
  preco DECIMAL(4,2) NULL DEFAULT NULL,
  data_coleta DATE NOT NULL,
  atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idcoleta),
  INDEX fk_coleta_postos_idx (postos_idpostos ASC),
  INDEX fk_coleta_combustivel_idx (combustivel_idcombustivel ASC),
  CONSTRAINT fk_coleta_postos
    FOREIGN KEY (postos_idpostos)
    REFERENCES postos (idpostos)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_coleta_combustivel
    FOREIGN KEY (combustivel_idcombustivel)
    REFERENCES combustivel (idcombustivel)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserir dados na tabela postos
INSERT INTO postos (nome_postos, bandeira, endereco, bairro, cidade, estado) VALUES
('Posto Torres', 'Torres', 'Av. Capixaba 47', 'Santa Inês', 'Vila Velha', 'ES'),
('Posto Canela Verde', 'Shell', 'Av. Carlos Lindenberg - Centro', 'Centro', 'Vila Velha', 'ES'),
('Posto Ciben Combustíveis', 'Petrobras', 'Rod. Do Sol 1796', 'Praia Itaparica', 'Vila Velha', 'ES'),
('Posto Champagnat', 'Ipiranga', 'Av. Hugo Musso 500', 'Praia da Costa', 'Vila Velha', 'ES'),
('Posto Ipiranga Santa Inês', 'Ipiranga', 'Av. Carlos Lindenberg 1801', 'Santa Inês', 'Vila Velha', 'ES'),
('Posto Ipiranga Rota 27', 'Ipiranga', 'Av. Anchieta 506', 'Av Anchieta', 'Guarapari', 'ES');

-- Inserir dados na tabela combustivel
INSERT INTO combustivel (tipo_combustivel) VALUES
('Gasolina Comum'),
('Gasolina Aditivada'),
('Etanol'),
('Diesel');

-- Inserir dados na tabela coleta
INSERT INTO coleta (postos_idpostos, combustivel_idcombustivel, preco, data_coleta) VALUES
(1, 1, 6.64, '2025-02-24'),
(1, 2, 6.84, '2025-02-24'),
(1, 3, 4.93, '2025-02-24'),
(1, 4, 6.45, '2025-02-24'),

(2, 1, 6.35, '2025-02-24'),
(2, 2, 6.45, '2025-02-24'),
(2, 3, 4.34, '2025-02-24'),
(2, 4, 6.27, '2025-02-24'),

(3, 1, 6.49, '2025-03-13'),
(3, 2, 6.59, '2025-03-13'),
(3, 3, 4.48, '2025-03-13'),
(3, 4, 6.39, '2025-03-13'),

(4, 1, 6.23, '2025-03-13'),
(4, 2, 6.65, '2025-03-13'),
(4, 3, 4.47, '2025-03-13'),
(4, 4, 6.39, '2025-03-13'),

(5, 1, 6.38, '2025-03-13'),
(5, 2, 6.58, '2025-03-13'),
(5, 3, 4.28, '2025-03-13'),
(5, 4, 6.39, '2025-03-13'),

(6, 1, 6.64, '2025-02-24'),
(6, 2, 6.84, '2025-02-24'),
(6, 3, 4.93, '2025-02-24'),
(6, 4, 6.45, '2025-02-24'
