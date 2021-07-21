--N

SELECT DISTINCT titles.title,authors.au_fname,authors.au_lname,(titles.royalty)*ytd_sales*price AS sales
FROM titles JOIN titleauthor ON titles.title_id = titles.title_id
JOIN authors ON authors.au_id = titleauthor.au_id
GROUP BY titles.title,authors.au_fname,authors.au_lname,titles.royalty,titles.ytd_sales,titles.price;