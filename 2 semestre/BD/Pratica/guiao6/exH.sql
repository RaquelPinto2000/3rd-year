-- h

SELECT publishers.pub_id,publishers.pub_name,SUM(titles.ytd_sales) AS sum_sales 
FROM publishers JOIN titles ON publishers.pub_id = titles.pub_id
GROUP BY publishers.pub_id, publishers.pub_name;