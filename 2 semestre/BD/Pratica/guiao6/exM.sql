--m)

SELECT titles.type
FROM titles
GROUP BY titles.type
HAVING MAX(advance)>AVG(advance)*1.5;