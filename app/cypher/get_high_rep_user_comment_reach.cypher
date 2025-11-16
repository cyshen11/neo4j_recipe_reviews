// Influential Commenter Analysis: What is the reach of a high-reputation user's comments? Find all users who have commented on the same recipes as the top 10 highest-reputation users. This can help identify which users are part of a key network.

// Find highest-reputation-users
MATCH (top_users:USER)
ORDER BY top_users.user_reputation DESC
LIMIT 10

WITH top_users
MATCH (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (top_users)
WHERE u.user_id <> top_users.user_id

RETURN 
    top_users.user_name, 
    top_users.user_reputation,
    collect(DISTINCT r.recipe_name) AS recipe_name, 
    collect(DISTINCT u.user_name) AS reach
;
