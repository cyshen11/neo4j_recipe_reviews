
// /**
//  * PURPOSE: Influential User Network Analysis - Identify Users Reached by a Specific High-Reputation User
//  * 
//  * This query measures the direct influence and network reach of a specific high-reputation user by finding
//  * all other users who have engaged in comment discussions on the same recipes. It filters results to only
//  * include users who share engagement on a minimum number of recipes, helping identify strong network connections.
//  * 
//  * RETURNS (for users influenced by the specified user):
//  *   - reached_user: Username of the influenced user
//  *   - recipe_count: Number of recipes where both users have commented
//  *   - reached_user_reputation: Reputation score of the influenced user
//  */

// STAGE 1: Identify the specific high-reputation user to analyze
MATCH (top_users:USER)
WHERE top_users.user_name = '{user}'

// STAGE 2: Find all other users who have commented on the same recipes as the specified user
WITH top_users
// Pattern: OTHER_USER -> posts COMMENT -> belongs to RECIPE <- commented by TARGET_USER
// This identifies the "reach" - all users engaged in the same recipe conversations
MATCH (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (top_users)
WHERE u.user_id <> top_users.user_id    // Exclude the target user themselves

// STAGE 3: Aggregate shared recipe count for each influenced user
WITH 
    u AS reached_user,
    count(DISTINCT r.recipe_name) AS recipe_count    // Count recipes where both users commented
// Filter to only significant connections (users sharing engagement on minimum recipe threshold)
WHERE recipe_count >= {recipe_count}

// STAGE 4: Return influence metrics with user reputation for network analysis
RETURN 
    reached_user.user_name AS reached_user,
    recipe_count,                                      // Strength of connection (shared recipe engagement)
    reached_user.user_reputation AS reached_user_reputation
ORDER BY recipe_count DESC                             // Show strongest connections first
;
