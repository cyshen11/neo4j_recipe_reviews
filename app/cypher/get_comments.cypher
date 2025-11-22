MATCH (r:RECIPE) <- [:BELONGS_TO] - (c:COMMENT) - [:POSTED] - (u:USER)
WHERE u.user_name = '{user}'

RETURN c.text AS comment, c.thumbs_up AS thumbs_up, c.created_at AS created_at, r.recipe_name AS recipe
ORDER BY c.thumbs_up DESC