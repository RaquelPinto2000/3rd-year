-- i)

SELECT p.pub_id, p.pub_name, t.title, SUM(t.ytd_sales) AS total_vendas
FROM publishers AS p JOIN titles AS t ON p.pub_id = t.pub_id
WHERE t.ytd_sales!= 0
GROUP BY p.pub_id,p.pub_name, t.title;