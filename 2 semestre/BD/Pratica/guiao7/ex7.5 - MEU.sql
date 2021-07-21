-- 7.5

--A)
-- i
CREATE VIEW BOOKS_TITLES_AUTHOR(title,author) AS
	SELECT titles.title, authors.au_fname+ ' ' +authors.au_lname
	FROM titles INNER JOIN titleauthor ON titles.title_id=titleauthor.title_id
	JOIN authors ON authors.au_id = titleauthor.au_id;
GO 

--ii
CREATE VIEW NAME_PUBLISHERS_EMPLOYEE(pub_name, emplo_name) AS
	SELECT publishers.pub_name, employee.fname + ' ' + employee.minit + '. ' + employee.lname
	FROM publishers JOIN employee ON publishers.pub_id=employee.pub_id;
GO

--iii
CREATE VIEW STORE_NAME_TITLES(store_name, book_name) AS
	SELECT stores.stor_name, titles.title
	FROM stores JOIN sales ON stores.stor_id=sales.stor_id JOIN titles ON sales.title_id=titles.title_id;
GO

--iV
CREATE VIEW BOOKS_BUSINESS(title_id,title,[type],pub_id,price,notes) AS
SELECT titles.title_id, titles.title, titles.[type],titles.pub_id, titles.price,titles.notes
FROM titles WHERE titles.[type] = 'Business'
WITH CHECK OPTION;
GO

--B)
--i
SELECT * FROM BOOKS_TITLES_AUTHOR WHERE title LIKE '%Enemy%';
GO

--ii
SELECT * FROM NAME_PUBLISHERS_EMPLOYEE WHERE pub_name LIKE '%Books%';
GO
--iii
SELECT * FROM STORE_NAME_TITLES WHERE store_name LIKE'%';
GO

--iv
SELECT * FROM BOOKS_BUSINESS WHERE title LIKE '%Computer%';
GO

--C)
--i
ALTER VIEW BOOKS_TITLES_AUTHOR(store_name,title,author) AS
	SELECT stores.stor_name,titles.title, authors.au_fname+ ' ' +authors.au_lname
	FROM titles INNER JOIN titleauthor ON titles.title_id=titleauthor.title_id
	JOIN authors ON authors.au_id = titleauthor.au_id
	JOIN sales ON sales.title_id=titles.title_id
	JOIN stores ON stores.stor_id=sales.stor_id;
GO 
--iii
ALTER VIEW STORE_NAME_TITLES(store_name, book_name,author) AS
	SELECT stores.stor_name, titles.title, authors.au_fname+ ' ' +authors.au_lname
	FROM stores JOIN sales ON stores.stor_id=sales.stor_id 
	JOIN titles ON sales.title_id=titles.title_id
	JOIN titleauthor ON titles.title_id=titleauthor.title_id
	JOIN authors ON authors.au_id=titleauthor.au_id;
GO


--D)
SELECT * FROM BOOKS_BUSINESS;

insert into BOOKS_BUSINESS (title_id, title, type, pub_id, price, notes)
values('BDTst1', 'New BD Book','popular_comp', '1389', $30.00, 'A must-read for
DB course.');

--i
-- Não obtivemos sucesso na execução, porque ...... 
-- para resolver o problema alteramos na alinea a .....
