SELECT COUNT(DISTINCT(people.name)) FROM stars JOIN (SELECT stars.movie_id, stars.person_id FROM people
JOIN stars ON stars.person_id=people.id
WHERE people.name='Kevin Bacon' AND people.birth=1958) as kevin_starred ON
stars.movie_id=kevin_starred.movie_id AND stars.person_id!=kevin_starred.person_id
JOIN people ON stars.person_id=people.id;




