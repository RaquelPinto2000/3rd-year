--p

SELECT titles.title,titles.ytd_sales,CONCAT(authors.au_fname,' ',authors.au_fname),
       (titles.royalty / 100.0) * (titles.ytd_sales * titles.price) * (titleauthor.royaltyper / 100.0) AS auth_revenue,
       ((titles.ytd_sales * titles.price) - (titles.royalty / 100.0 * titles.ytd_sales * titles.price)) AS publisher_revenue
FROM	titles JOIN titleauthor ON titles.title_id=titleauthor.title_id
		JOIN authors ON authors.au_id = titleauthor.au_id
WHERE ytd_sales>0;