-- a
CREATE PROCEDURE Delete_Employee(@ssn INT)
AS
BEGIN
	BEGIN TRANSACTION;
		DELETE FROM works_on WHERE Essn=@ssn;
		DELETE FROM [dependent] WHERE Essn=@ssn;
		UPDATE department set Mgr_ssn=NULL WHERE Essn=@ssn;
		UPDATE employee set Super_ssn=NULL WHERE Essn=@ssn;
		DELETE FROM employee WHERE Ssn=@ssn;
	COMMIT;
END
GO

-- b
CREATE PROCEDURE OldSsn(@ssn INT output,@year_count INT output)
AS 
BEGIN
	SELECT Fname,Lname,Dname,Mgr_start_date
	FROM department 
	INNER JOIN employee ON Mgr_snn=Ssn 
	ORDER BY Mgr_start_date;

	SELECT TOP(1) @ssn=ssn,@year_count=DATEDIFF(yy,GETDATE(),Mgr_start_date)
	FROM department 
	INNER JOIN employee ON Mgr_ssn=Ssn
	ORDER BY Mgr_start_date;

	-- ou
	/*SELECT Fname, Lname, Dname, Mgr_start_date, @OldSsn=Ssn, @OldYear=DATEDIFF(YEAR,GETDATE(),Mgr_state_sate)
		FROM department INNER JOIN
			employee ON Mgr_ssn=Ssn
		ORDER BY Mgr_start_date DESC
		*/
END
GO

--c
CREATE TRIGGER Mgr_department ON department
INSTEAD OF INSERT
AS 
BEGIN
	DECLARE @ssn_val as INT; 
	SELECT @ssn_val=Mgr_ssn FROM inserted;
	/*
	UPDATE department 
	SET Mgr_ssn = NULL 
	FROM(
		SELECT Mgr_ssn,Dnumber 
		FROM department 
		WHERE 
		) as dep_query
	WHERE @dno_val = dep_query.Mgr_ssn and dep_query.Dnumber=@dno_val
	*/
	
	IF EXISTS(SELECT Mgr_ssn FROM department WHERE @ssn_val=Mgr_ssn)
		BEGIN
			RAISERROR('Employee already manages another department');
			ROLLBACK TRAN;
		END
	ELSE	
		BEGIN
			INSERT INTO department SELECT * FROM inserted;
		END
END
GO

-- d
CREATE TRIGGER Limit_Salary ON employee
AFTER INSERT, UPDATE
AS
BEGIN
	DECLARE @salary_val as INT; 
	DECLARE @ssn_val as INT; 
	DECLARE @dno_val as INT;

	SELECT @ssn_val=Ssn,@salary_val=Salary,@dno_val=Dno FROM inserted;

	UPDATE employee
	SET Salary= mgr_query.Salary-1
	FROM
		(SELECT Salary,ssn
		FROM employee,department
		WHERE employee.Dno=@dno_val and employee.Dno=department.Dnumber 
			and employee.Ssn=department.Mgr_ssn
		) as mgr_query
	WHERE @salary_val>=mgr_query.Salary and mgr_query.ssn=@ssn_val;
END
GO

-- e
CREATE FUNCTION Name_location(@ssn_employee int) RETURNS @table TABLE (nome VARCHAR(250), localizacao VARCHAR(250))
AS
	BEGIN
		INSERT @table SELECT project.Pname, project.Plocation
				FROM project JOIN works_on ON project.Pnumber=works_on.Pno
				WHERE works_on.Essn = @ssn_employee
		RETURN;
	END;
GO


-- f
CREATE FUNCTION Average_Salary(@dno INT) 
RETURNS Table
AS
	RETURN(	SELECT Ssn,Salary  
			FROM employee
			JOIN (	SELECT AVG(Salary) as avg_salary 
					FROM employee 
					WHERE Dno=1) AS avg_query 
			ON Dno=1 and Salary >= avg_query.avg_salary
			);
GO

--g
CREATE FUNCTION alineaG (@dno_project int) RETURNS @table TABLE (nome_projeto VARCHAR (250), budget INT, totalbudget INT)
AS
	BEGIN
		INSERT @table 
			SELECT project.Pname, SUM(employee.Salary) AS budget, SUM(employee.Salary*works_on.Hours) AS totalbudget
			FROM department
				JOIN project ON project.Dnum=department.Dnumber
				JOIN works_on ON works_on.Pno=project.Pnumber
				JOIN employee ON employee.Ssn=works_on.Essn
			GROUP BY project.Pname

		RETURN;
	END;
GO

-- h
CREATE TRIGGER Remove_After ON department
AFTER DELETE, UPDATE
AS
	IF NOT (EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='myschema'AND TABLE_NAME = 'Deleted_Department'))
		CREATE TABLE Deleted_Department(
			Dname				VARCHAR(250) NOT NULL,
			Dnumber				INT,
			Mgr_ssn				INT,
			Mgr_start_date		DATE,
			PRIMARY KEY (Dnumber)
		);

	INSERT INTO Deleted_Department SELECT * FROM deleted;
GO

CREATE TRIGGER Remove_Before ON department
INSTEAD OF DELETE
AS
BEGIN

	IF NOT (EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='myschema'AND TABLE_NAME = 'Deleted_Department'))
		CREATE TABLE Deleted_Department(
			Dname				VARCHAR(250) NOT NULL,
			Dnumber				INT,
			Mgr_ssn				INT,
			Mgr_start_date		DATE,
			PRIMARY KEY (Dnumber)
		);
	DECLARE @deleted_dno INT
	SELECT @deleted_dno=Dnumber FROM deleted
	DELETE FROM department WHERE Dnumber=@deleted_dno
	INSERT INTO Deleted_Department SELECT * FROM deleted;
END
GO

-- Podemos concluir que o trigger "Instead of" necessita de uma Query de DELETE (precisa de apagar a row para além de inserir na table Deleted_Department)
--enquanto que o After já não necessita de tal Query (só tem de inserir na Deleted_Department).

-- i
-- documento pdf