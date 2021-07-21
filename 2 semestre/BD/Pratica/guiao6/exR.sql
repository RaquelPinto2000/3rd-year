-- r

SELECT stor_id, stor_name, avg_sales
FROM (SELECT AVG(qty) AS all_avg_sales FROM sales AS sal JOIN stores as s ON sal.stor_id = s.stor_id ) AS avg_all
JOIN (SELECT s.stor_id, stor_name, AVG(qty) AS avg_sales
		FROM sales AS sal JOIN stores as s ON sal.stor_id=s.stor_id
		GROUP BY s.stor_id, s.stor_name) AS avg_each ON avg_sales > all_avg_sales