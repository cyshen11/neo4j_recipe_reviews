MATCH (r1:RECIPE) <- [:BELONGS_TO] - (:COMMENT) -  [:POSTED] - (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r2:RECIPE)
WHERE r1.recipe_name <> r2.recipe_name
AND r1.recipe_name = '{recipe}'

RETURN 
    DISTINCT r2.recipe_name AS recipe_name,
    COUNT(DISTINCT u) AS user_count
ORDER BY user_count DESC
;