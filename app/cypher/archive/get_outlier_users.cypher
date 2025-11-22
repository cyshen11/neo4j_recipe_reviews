MATCH (u1:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)
OPTIONAL MATCH (u2:USER)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r)
WHERE u1 <> u2

WITH u1.user_name AS user_name, r.recipe_name AS recipe_name, COUNT(u2) AS shared_commenters_count
ORDER BY shared_commenters_count ASC

RETURN 
    user_name,
    recipe_name,
    shared_commenters_count
LIMIT 1000