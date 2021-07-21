CREATE SCHEMA STOCKS;
GO

CREATE TABLE STOCKS.produto(
	codigo		INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	preco		DECIMAL(9,0) CHECK(preco > 0) NOT NULL,
	nome		VARCHAR(256) NOT NULL,
	taxa_iva	INT CHECK(taxa_iva >=0 and taxa_iva<=100),
	no_unidades INT NOT NULL
);
GO

CREATE TABLE STOCKS.tipo_fornecedor(
	codigo_interno  INT PRIMARY KEY NOT NULL,
	designacao		VARCHAR(256) NOT NULL
);
GO

CREATE TABLE STOCKS.fornecedor(
	nif					DECIMAL(9,0) PRIMARY KEY CHECK(nif > 0) NOT NULL,
	condicoes_pagamento VARCHAR(1024) NOT NULL,
	nome				VARCHAR(256) NOT NULL,
	endereco			VARCHAR(1024) NOT NULL,
	no_fax				DECIMAL(9,0) UNIQUE CHECK(no_fax > 0) NOT NULL,
	tipo				INT FOREIGN KEY REFERENCES STOCKS.tipo_fornecedor(codigo_interno) NOT NULL 
);
GO

CREATE TABLE STOCKS.encomenda(
	no_encomenda	INT PRIMARY KEY NOT NULL,
	fornecedor		DECIMAL(9,0) REFERENCES STOCKS.fornecedor(nif) NOT NULL,
	data_encomenda  DATE NOT NULL
);
GO

CREATE TABLE STOCKS.armazem(
	codigo		 INT PRIMARY KEY REFERENCES STOCKS.produto(codigo) NOT NULL,
	localizacao	 INT NOT NULL,
	nome		 VARCHAR(256) NOT NULL,
	no_encomenda INT FOREIGN KEY REFERENCES STOCKS.encomenda(no_encomenda) NOT NULL
);
GO