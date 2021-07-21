-- s)

SELECT t.title
FROM titles AS t JOIN sales as sal ON t.title_id=sal.title_id JOIN stores AS s ON s.stor_id=sal.stor_id
WHERE s.stor_name!='Bookbeat';