MATCH
    (r1:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r2:RECIPE)
WHERE
    r1.recipe_name <> r2.recipe_name
    AND r2.recipe_name = '{recipe}'

RETURN
    r1.recipe_name AS recipe_name,
    COUNT(DISTINCT u) AS shared_commenter_count,
    COLLECT(DISTINCT u.user_name) AS shared_commenters
ORDER BY shared_commenter_count DESC
LIMIT 5
;