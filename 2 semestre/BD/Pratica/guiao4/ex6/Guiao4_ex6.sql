CREATE SCHEMA ATL;
GO

CREATE TABLE ATL.atl(
	identificador INT PRIMARY KEY NOT NULL,
	classes INT NOT NULL
);
GO

CREATE TABLE ATL.pessoa(
	email VARCHAR(250) UNIQUE NOT NULL,
	nome VARCHAR(250) NOT NULL,
	no_cc INT PRIMARY KEY NOT NULL CHECK(no_cc>0),
	morada VARCHAR(250) NOT NULL,
	data_nascimento DATE NOT NULL
);
GO

CREATE TABLE ATL.professor(
	no_funcionario INT PRIMARY KEY NOT NULL,
	no_cc INT REFERENCES ATL.pessoa(no_cc) NOT NULL,
	telefone INT NOT NULL
);
GO

CREATE TABLE ATL.encarregado_educacao(
	no_cc INT PRIMARY KEY REFERENCES ATL.pessoa(no_cc) NOT NULL,
	relacao_aluno VARCHAR(50),
	telefone INT NOT NULL
);
GO

CREATE TABLE ATL.lista_pessoas_autorizadas(
	no_cc INT PRIMARY KEY REFERENCES ATL.pessoa(no_cc) NOT NULL,
	telefone INT NOT NULL
);
GO

CREATE TABLE ATL.turma(
	identificador_atl INT REFERENCES ATL.atl(identificador) NOT NULL,
	identificador INT PRIMARY KEY NOT NULL,
	no_funcionario INT REFERENCES ATL.professor(no_funcionario) NOT NULL,
	no_max_alunos INT NOT NULL,
	designacao	VARCHAR(50) NOT NULL,
	ano_letivo  INT NOT NULL,
	identificador_atividade INT REFERENCES ATL.atividade(identificador) NOT NULL
);
GO

CREATE TABLE ATL.aluno(
	no_cc INT PRIMARY KEY REFERENCES ATL.pessoa(no_cc) NOT NULL,
	identificador INT REFERENCES ATL.turma(identificador) NOT NULL,
	cc_encarregado INT FOREIGN KEY REFERENCES ATL.encarregado_educacao(no_cc) NOT NULL
);
GO

CREATE TABLE ATL.atividade(
	custo INT NOT NULL,
	designacao VARCHAR(250) NOT NULL,
	identificador INT PRIMARY KEY NOT NULL,
	turma INT NOT NULL CHECK(turma>0),
	alunos VARCHAR(250) NOT NULL
);
GO
