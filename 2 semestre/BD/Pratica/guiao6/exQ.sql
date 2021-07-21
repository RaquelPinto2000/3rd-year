--q)

SELECT stor_id, stor_name, titulos_vendidos
FROM (SELECT COUNT(t.title_id) AS total_livros FROM titles AS t) AS total_livros
	JOIN (SELECT s.stor_id, s.stor_name, COUNT(t.title_id) AS titulos_vendidos 
	FROM (titles AS t JOIN sales AS sal ON t.title_id=sal.title_id JOIN stores AS s ON s.stor_id=sal.stor_id)
GROUP BY s.stor_id, s.stor_name) AS loja ON total_livros=titulos_vendidos;