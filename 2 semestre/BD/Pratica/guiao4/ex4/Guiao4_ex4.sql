CREATE SCHEMA Guiao4_ex4;
GO

CREATE TABLE Guiao4_ex4.Medico(
	Medico_Nome			VARCHAR(50)				NOT NULL,
	Especialidade		VARCHAR(100)			NOT NULL,
	ID					INT		PRIMARY KEY		NOT NULL
);
GO

CREATE TABLE Guiao4_ex4.Paciente(
	Paciente_Nome			VARCHAR(50)			NOT NULL,
	Data_Nascimento			DATE				NOT NULL,
	Paciente_Endereco		VARCHAR(200)		NOT NULL,
	Num_Utente				INT		PRIMARY KEY NOT NULL,
);
GO

CREATE TABLE Guiao4_ex4.Companhia(
	Companhia_Nome			VARCHAR(50)				NOT NULL,
	Companhia_Endereco		VARCHAR(200)			NOT NULL,
	Companhia_Telefone		VARCHAR(13)				NOT NULL,
	Comp_Registo			VARCHAR(30)	PRIMARY KEY NOT NULL,
);
GO

CREATE TABLE Guiao4_ex4.Farmaco(
	Formula							VARCHAR(100)	NOT NULL,
	Farmaco_Nome					VARCHAR(50)		NOT NULL,	
	Companhia_Registo				VARCHAR(30)		FOREIGN KEY REFERENCES Guiao4_ex4.Companhia(Comp_Registo) NOT NULL,
	Farmaco_Codigo					INT				PRIMARY KEY NOT NULL,		
);
GO

CREATE TABLE Guiao4_ex4.Farmacia(
	Farm_Nome				VARCHAR(50)					NOT NULL,
	Farm_Telefone			VARCHAR(13)					NOT NULL,
	Farm_Endereco			VARCHAR(200)				NOT NULL,
	Codigo_Farmaco			INT	REFERENCES Guiao4_ex4.Farmaco(Farmaco_Codigo) NOT NULL,
	Farm_NIF				INT			PRIMARY KEY		NOT NULL,
);
GO

CREATE TABLE Guiao4_ex4.Prescricao(
	Pres_Data		DATE					NOT NULL,	
	Num_Utente		INT 	REFERENCES Guiao4_ex4.Paciente(Num_Utente) NOT NULL,
	ID_medico		INT		REFERENCES Guiao4_ex4.Medico(ID) NOT NULL,	
	NIF_Farmacia	INT		REFERENCES Guiao4_ex4.Farmacia(Farm_NIF) NOT NULL,
	Pres_Codigo		INT		PRIMARY KEY		NOT NULL,
);

CREATE TABLE Guiao4_ex4.Prescrevido(
	--- Relacao entre prescricao e farmaco 
	Prescricao_Code	INT REFERENCES Guiao4_ex4.Prescricao(Pres_Codigo) NOT NULL,
	Farmaco_Code	INT REFERENCES Guiao4_ex4.Farmaco(Farmaco_Codigo) NOT NULL,
	PRIMARY KEY(Prescricao_Code,Farmaco_Code)
);
GO

CREATE TABLE Guiao4_ex4.Levantado(
	--- Relacao entre farmacia e farmaco
	Farmacia_NIF	INT REFERENCES Guiao4_ex4.Farmacia(Farm_NIF) NOT NULL,
	Farmaco_Code	INT REFERENCES Guiao4_ex4.Farmaco(Farmaco_Codigo) NOT NULL,
	PRIMARY KEY(Farmacia_NIF,Farmaco_Code)
);
GO