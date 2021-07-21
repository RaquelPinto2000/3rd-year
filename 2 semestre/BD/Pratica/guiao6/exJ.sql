--j

SELECT DISTINCT title FROM 
titles JOIN sales ON titles.title_id=sales.title_id
JOIN stores ON stores.stor_id = sales.stor_id
WHERE stor_name = 'Bookbeat'