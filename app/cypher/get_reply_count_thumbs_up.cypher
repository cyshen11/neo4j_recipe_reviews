// Find high reputation users
MATCH (top_users:USER)
ORDER BY top_users.user_reputation DESC
LIMIT 100

// Get the first 5 star comment from the high reputation users
MATCH (r:RECIPE) <- [:BELONGS_TO] - (c1:COMMENT) - [:POSTED] - (top_users)
WHERE c1.stars = 5
AND r.recipe_name = '{recipe}'
ORDER BY c1.created_at
LIMIT 1

// Get the comments after the first 5 star comment 
MATCH (r) <- [:BELONGS_TO] - (c2:COMMENT) 
WHERE c2.created_at > c1.created_at

RETURN 
    top_users.user_name AS user,
    top_users.user_reputation AS user_reputation,
    c1.text AS comment,
    c1.created_at AS created_at,
    SUM(c2.reply_count) AS total_reply_count, 
    SUM(c2.thumbs_up) AS total_thumbs_up
;