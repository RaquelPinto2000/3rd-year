-- alinea a

CREATE PROCEDURE alineaA
	@in_ssn int
	--parametros de entrada e saida
AS 
BEGIN
	BEGIN TRANSACTION 
		UPDATE department SET Mgr_ssn NULL WHERE Mgr_ssn=@in_ssn;
		UPDATE employee SET Super_ssn NULL WHERE Super_ssn=@in_ssn;
		DELETE FROM works_on WHERE Essn=@in_ssn;
		DELETE FROM works_on_dependent WHERE Essn=@in_ssn;
		DELETE FROM employee WHERE Ssn=@in_ssn;
	COMMIT;
END
GO

-- alinea b
CREATE PROCEDURE alineaB
	--@Mgr_ssn INT	
	@OldSsn int out,
	@OldYear int out
AS 
BEGIN
	--record set
	SELECT Fname, Lname, Dname, Mgr_start_date
		FROM department INNER JOIN 
			employee ON  Mgr_ssn=Ssn
		GROUP BY Mgr_start_date

	--o mais antigo e o primeiro do top
	SELECT TOP(1) @OldSsn=Ssn, @OldYear=DATEDIFF(YEAR,GETDATE(),Mgr_state_sate)
		FROM department INNER JOIN
			employee ON Mgr_ssn=Ssn
		ORDER BY Mgr_start_date


	-- ou
	/*SELECT Fname, Lname, Dname, Mgr_start_date, @OldSsn=Ssn, @OldYear=DATEDIFF(YEAR,GETDATE(),Mgr_state_sate)
		FROM department INNER JOIN
			employee ON Mgr_ssn=Ssn
		ORDER BY Mgr_start_date DESC
		*/
END
GO

-- alinea c -> nao esta acabada
CREATE TRIGGER alineaC on department
INSTEAD OF INSERT 
AS 
BEGIN
	SELECT Dnumber, count(Mgr_ssn) FROM n ON DEPARTMENT GROUP BY Dnumber
	
END


GO


-- alinea e

CREATE FUNCTION alineaE (@ssn_employee int) RETURNS @table TABLE (nome VARCHAR(250), localizacao VARCHAR(250))
AS
	BEGIN
		INSERT @table SELECT project.Pname, project.Plocation
				FROM project JOIN works_on ON project.Pnumber=works_on.Pno
				WHERE works_on.Essn = @ssn_employee
		RETURN;
	END;
GO


-- alinea g

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

--alinea i
-- documento pdf