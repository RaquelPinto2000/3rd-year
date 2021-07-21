DBCC FREEPROCCACHE;
DBCC DROPCLEANBUFFERS;

GO
--ex1
--select * from Production.WorkOrder
--GO

--ex2
--select * from Production.WorkOrder where WorkOrderID=1234
--GO

--ex3a
--SELECT * FROM Production.WorkOrder WHERE WorkOrderID between 10000 and 10010
--GO

--ex3b
--SELECT * FROM Production.WorkOrder WHERE WorkOrderID between 1 and 72591
--GO

--ex4
--SELECT * FROM Production.WorkOrder WHERE StartDate = '2007-06-25'
--GO

--ex5
--SELECT * FROM Production.WorkOrder WHERE ProductID = 757
--GO

--ex6a
--SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 757
--GO

--ex6b
--SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945
--GO

--ex6c
--SELECT WorkOrderID FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04'
--GO

--ex7
--SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04'
--GO

--ex8
--SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04'
--GO