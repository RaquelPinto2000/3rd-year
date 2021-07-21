CREATE SCHEMA RENT_A_CAR;
GO

CREATE TABLE RENT_A_CAR.cliente(
	nome		VARCHAR(256) NOT NULL,
	endereco	VARCHAR(1024) NOT NULL,
	num_carta	DECIMAL(9,0) UNIQUE NOT NULL CHECK(num_carta > 0),
	nif			DECIMAL(9,0) PRIMARY KEY NOT NULL CHECK(nif > 0)
);
GO

CREATE TABLE RENT_A_CAR.balcao(
	numero	 INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	nome	 VARCHAR(256) NOT NULL,
	endereco VARCHAR(1024) NOT NULL
);
GO

CREATE TABLE RENT_A_CAR.tipo_veiculo(
	codigo			INT PRIMARY KEY NOT NULL,
	designacao		VARCHAR(256) NOT NULL,
	arcondicionado  BIT NOT NULL
);
GO

CREATE TABLE RENT_A_CAR.veiculo(
	matricula VARCHAR(8) PRIMARY KEY NOT NULL,
	ano		  INT NOT NULL,
	marca	  VARCHAR(256) NOT NULL,
	codigo_v  INT FOREIGN KEY REFERENCES RENT_A_CAR.tipo_veiculo(codigo) NOT NULL
);
GO

CREATE TABLE RENT_A_CAR.aluguer(
	numero				INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	duracao				INT NOT NULL,
	aluguer_data		DATE NOT NULL,
	cliente_nif			DECIMAL(9,0) FOREIGN KEY REFERENCES RENT_A_CAR.cliente(nif) NOT NULL,
	b_numero			INT FOREIGN KEY REFERENCES RENT_A_CAR.balcao(numero) NOT NULL,
	aluguer_matricula	VARCHAR(8) FOREIGN KEY REFERENCES RENT_A_CAR.veiculo(matricula) NOT NULL
);
GO

CREATE TABLE RENT_A_CAR.ligiero(
	codigo			INT PRIMARY KEY FOREIGN KEY REFERENCES RENT_A_CAR.tipo_veiculo(codigo) NOT NULL,
	portas			INT NOT NULL,
	combustivel		VARCHAR(256),
	numlugares		INT NOT NULL
);

CREATE TABLE RENT_A_CAR.pesado(
	codigo		INT PRIMARY KEY FOREIGN KEY REFERENCES RENT_A_CAR.tipo_veiculo(codigo) NOT NULL,
	peso		INT NOT NULL,
	passageiros INT NOT NULL
);
GO

CREATE TABLE RENT_A_CAR.simularidade(
	codigo_a INT REFERENCES RENT_A_CAR.tipo_veiculo(codigo) NOT NULL,
	codigo_b INT REFERENCES RENT_A_CAR.tipo_veiculo(codigo) NOT NULL,
	PRIMARY KEY (codigo_a, codigo_b)
);
GO