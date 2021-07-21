--g)

SELECT DISTINCT publishers.pub_name
FROM publishers INNER JOIN titles on publishers.pub_id=titles.pub_id
WHERE[Type]='business'