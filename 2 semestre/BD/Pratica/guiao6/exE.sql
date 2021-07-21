-- e

SELECT au_fname AS first_name, au_lname AS last_name, phone AS telephone FROM authors WHERE state='CA' AND au_fname!='Ringer' ORDER BY first_name,last_name;