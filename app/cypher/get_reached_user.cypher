// Influential Commenter Analysis: What is the reach of a high-reputation user's comments? Find all users who have commented on the same recipes as the top 10 highest-reputation users. This can help identify which users are part of a key network.

// Find highest-reputation-users
MATCH (top_users:USER)
WHERE top_users.user_name = '{user}'

WITH top_users
MATCH (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (top_users)
WHERE u.user_id <> top_users.user_id

WITH 
    u AS reached_user,
    count(DISTINCT r.recipe_name) AS recipe_count
WHERE recipe_count >= {recipe_count}

RETURN 
    reached_user.user_name AS reached_user,
    recipe_count,
    reached_user.user_reputation AS reached_user_reputation
ORDER BY recipe_count DESC
;
