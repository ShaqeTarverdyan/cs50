SELECT title, year FROM movies
WHERE title LIKE "Harry Potter%"
ORDER BY year ASC;


SELECT COUNT(title) FROM movies
WHERE title LIKE "Harry Potter%";
