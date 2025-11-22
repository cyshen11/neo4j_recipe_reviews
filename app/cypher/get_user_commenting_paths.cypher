MATCH (r1:RECIPE) <- [:BELONGS_TO] - (c1:COMMENT) - [:POSTED] - (u:USER)
WHERE r1.recipe_name = '{recipe}'

MATCH (u)-[:POSTED]-(c2:COMMENT)-[:BELONGS_TO]->(r2:RECIPE)
WHERE c2 <> c1
AND r2 <> r1

WITH u.user_name AS user,
    r1.recipe_name AS recipe1,
    c1.created_at AS created1,
    COLLECT({recipe: r2.recipe_name, created: c2.created_at}) AS other_comments

WITH user,
    [{recipe: recipe1, created: created1}] + other_comments AS comments

UNWIND comments AS c
WITH user, c.recipe AS recipe, c.created AS created
ORDER BY user, created

WITH user,
    COLLECT(DISTINCT recipe) AS commenting_path

WITH commenting_path,
    COUNT(user) AS user_count
WHERE user_count > 1

RETURN
    commenting_path,
    user_count
ORDER BY user_count DESC
;