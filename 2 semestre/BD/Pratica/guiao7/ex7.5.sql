-- 7.5

--A)
-- i
CREATE VIEW BOOKS_TITLES_AUTHOR(title,author) AS
	SELECT titles.title, authors.au_fname+ ' ' +authors.au_lname
	FROM titles INNER JOIN titleauthor ON titles.title_id=titleauthor.title_id
	JOIN authors ON authors.au_id = titleauthor.au_id;
GO 

--ii
CREATE VIEW PUB_EMPLOYEE(pub_name,empl_name) AS
	SELECT publishers.pub_name,employee.fname + ' ' + employee.lname
	FROM publishers JOIN employee ON publishers.pub_id=employee.emp_id
GO

--iii
CREATE VIEW STORE_NAME_TITLES(store_name, book_name) AS
	SELECT stores.stor_name, titles.title
	FROM stores JOIN sales ON stores.stor_id=sales.stor_id JOIN titles ON sales.title_id=titles.title_id;
GO

--iV
CREATE VIEW titles_business(title_id, title, type, pub_id, price, notes) AS
	SELECT titles.title_id, titles.title, titles.type, titles.pub_id, titles.price, titles.notes
	FROM titles
	WHERE type = 'BUSINESS'
	WITH CHECK OPTION; 
GO

--B)
--i
SELECT * FROM BOOKS_TITLES_AUTHOR WHERE title LIKE '%Enemy%';
GO

--ii
SELECT *
FROM PUB_EMPLOYEE
WHERE pub_name LIKE '%BOOKS%';

--iii
SELECT * FROM STORE_NAME_TITLES WHERE store_name LIKE'%';
GO

--iv
SELECT *
FROM titles_business
WHERE title LIKE '%Computer%';
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
-- d) iv 
-- ii. Altere a view (iv da alínea a) para corrigir o problema.
-- podemos remover o CHECK OPTION
CREATE VIEW titles_business_d(title_id, title, type, pub_id, price, notes) AS
	SELECT titles.title_id, titles.title, titles.type, titles.pub_id, titles.price, titles.notes
	FROM titles
	WHERE type = 'BUSINESS';
	--WITH CHECK OPTION; 
GO

--SELECT *
--FROM titles_business
--insert into titles_business(title_id, title, type, pub_id, price, notes) 
--values('BDTst1', 'New BD Book','BUSINESS', '1389', $30.00, 'A must-read for DB course.')

-- i. Teve sucesso na sua execução? Faz sentido?
-- o comando não teve sucesso pela existencia do CHECK OPTION que vai impedir adicionar 
-- objetos com o type diferente de 'BUSINESS'

-- ii. Altere a view (iv da alínea a) para corrigir o problema.
-- podemos remover o CHECK OPTION

-- iii. Volte a testar a instrução acima.

SELECT *
FROM titles_business_d
insert into titles_business_d(title_id, title, type, pub_id, price, notes) 
	values('BDTst1', 'New BD Book','BUSINESS', '1389', $30.00, 'A must-read for DB course.');
