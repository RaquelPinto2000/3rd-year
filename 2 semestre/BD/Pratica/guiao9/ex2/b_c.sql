-- alinea B e C

--drop table mytemp;

CREATE TABLE mytemp (
	rid BIGINT /*IDENTITY (1, 1)*/ NOT NULL,
	at1 INT NULL,
	at2 INT NULL,
	at3 INT NULL,
	lixo varchar(100) NULL,
	primary key clustered (rid) with (fillfactor = 90) 
);

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
	INSERT mytemp (rid, at1, at2, at3, lixo)
	SELECT cast((RAND()*@nelem*40000) as int), cast((RAND()*@nelem) as int),
		   cast((RAND()*@nelem) as int), cast((RAND()*@nelem) as int),
		   'lixo...lixo...lixo...lixo...lixo...lixo...lixo...lixo...lixo';
	SET @val = @val + 1;
END

PRINT 'Inserted ' + str(@nelem) + ' total records'

-- Duration of Insertion Process
SET @end_time = GETDATE();	
PRINT 'Milliseconds used: ' + CONVERT(VARCHAR(20), DATEDIFF(MILLISECOND,
@start_time, @end_time));

--

--b)
/*Inserted      50000 total records
Milliseconds used: 68376
Page fullness -> 70,55 %
Total fragmentation -> 99,26 %
*/

--c)
/*

fillfactor = 65
Inserted      50000 total records
Milliseconds used: 72126
Page fullness -> 69,61 %
Total fragmentation -> 99,39 %


fillfactor = 80
Inserted      50000 total records
Milliseconds used: 72566
Page fullness -> 67,48 %
Total fragmentation -> 98,71 %


fillfactor = 90
Inserted      50000 total records
Milliseconds used: 71100
Page fullness -> 68,86 %
Total fragmentation -> 98,68 %
*/
