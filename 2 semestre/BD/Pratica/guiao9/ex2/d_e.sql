-- alinea D e E

--drop table mytemp;

CREATE TABLE mytemp (
	rid BIGINT IDENTITY (1, 1) NOT NULL,
	at1 INT NULL,
	at2 INT NULL,
	at3 INT NULL,
	lixo varchar(100) NULL,
	primary key clustered (rid) -- with (fillfactor = 90) 
);

create index at1 on mytemp(at1);
create index at2 on mytemp(at2);
create index at3 on mytemp(at3);
create index lixo on mytemp(lixo);


-- Record the Start Time
DECLARE @start_time DATETIME, @end_time DATETIME;
SET @start_time = GETDATE();
PRINT @start_time

-- Generate random records
DECLARE @val as int = 1;
DECLARE @nelem as int = 50000;

SET nocount ON
WHILE @val <= @nelem
BEGIN
	DBCC DROPCLEANBUFFERS;						-- need to be sysadmin
	INSERT mytemp (/*rid,*/ at1, at2, at3, lixo)
	SELECT /*cast((RAND()*@nelem*40000) as int),*/ cast((RAND()*@nelem) as int),
		   cast((RAND()*@nelem) as int), cast((RAND()*@nelem) as int),
		   'lixo...lixo...lixo...lixo...lixo...lixo...lixo...lixo...lixo';
	SET @val = @val + 1;
END

PRINT 'Inserted ' + str(@nelem) + ' total records'

-- Duration of Insertion Process
SET @end_time = GETDATE();	
PRINT 'Milliseconds used: ' + CONVERT(VARCHAR(20), DATEDIFF(MILLISECOND, @start_time, @end_time));

--d
/*
Inserted      50000 total records
Milliseconds used: 63016
*/

--e
/*
Inserted      50000 total records
Milliseconds used: 92166


O uso de índices melhora o tempo de consulta, contudo aumenta o tempo de inserção. 
Por isso, o tempo na inserção com índices (alínea E -> 92166 ms) foi maior do que na inserção
sem índices (alínea D -> 63016 ms)

*/
