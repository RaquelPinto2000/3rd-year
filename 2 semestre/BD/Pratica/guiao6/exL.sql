-- l

SELECT titles.type,AVG(titles.price) as total_types, SUM(DISTINCT titles.ytd_sales) as total_publishers 
FROM titles WHERE type != 'UNDECIDED'
GROUP BY titles.type,titles.pub_id;