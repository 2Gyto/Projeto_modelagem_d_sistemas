-- 1. Criação da tabela de Usuários
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE, 
    senha_hash VARCHAR(255) NOT NULL,   
    ativo BOOLEAN DEFAULT TRUE,         
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Criação da tabela principal do projeto (Agora vinculada ao usuário)
CREATE TABLE simulacao (
    id_simulacao INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL, -- Chave que conecta a simulação ao dono da conta
    nome_projeto VARCHAR(100) NOT NULL,
    
    -- Localização (coordenadas para cálculo solar)
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Instalação
    largura_telhado_m DECIMAL(5, 2),
    comprimento_telhado_m DECIMAL(5, 2),
    tipo_rede VARCHAR(20), 
    nivel_sombreamento VARCHAR(20), 
    modalidade VARCHAR(20), 
    
    -- Dados Financeiros
    tarifa_energia DECIMAL(5, 4), 
    inflacao_estimada DECIMAL(5, 2), 
    
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Chave estrangeira ligando a simulação ao usuário
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- 3. Criação da tabela secundária para armazenar os 12 meses de consumo
CREATE TABLE historico_consumo (
    id_consumo INT PRIMARY KEY AUTO_INCREMENT,
    id_simulacao INT NOT NULL,
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12), 
    consumo_kwh DECIMAL(8, 2) NOT NULL,
    
    -- Chave estrangeira ligando o consumo à simulação
    FOREIGN KEY (id_simulacao) REFERENCES simulacao(id_simulacao) ON DELETE CASCADE
);