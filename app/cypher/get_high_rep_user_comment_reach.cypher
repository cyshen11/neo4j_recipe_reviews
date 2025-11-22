
// /*
//  * PURPOSE: Influential Commenter Analysis - Measure the reach of high-reputation users' comments
//  * 
//  * This query identifies the top N highest-reputation users and determines their influence by
//  * finding all other users who have engaged in the same recipe comment conversations. This reveals
//  * key network hubs where influential users drive community engagement.
//  * 
//  * RETURNS (for each high-reputation user):
//  *   - user_name: Name of the high-reputation user
//  *   - user_reputation: Reputation score of the high-reputation user
//  *   - recipe_name: List of recipes discussed by the high-reputation user
//  *   - reach: Count of distinct users influenced (commenting on same recipes)
//  *   - users_reached: List of usernames of influenced users
//  */

// STAGE 1: Identify the top N highest-reputation users, ordered by their reputation score descending
MATCH (top_users:USER)
ORDER BY top_users.user_reputation DESC
LIMIT {n}

// STAGE 2: For each high-reputation user, find all other users in the same recipe comment network
WITH top_users
// Pattern: OTHER_USER -> posts COMMENT -> belongs to RECIPE <- commented by TOP_USER
// This identifies users who have commented on recipes that the high-reputation user also commented on
MATCH (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (top_users)

// Exclude the high-reputation user themselves from the reach count
WHERE u.user_id <> top_users.user_id

// STAGE 3: Aggregate and return results grouped by high-reputation user
RETURN 
    top_users.user_name, 
    top_users.user_reputation,
    collect(DISTINCT r.recipe_name) AS recipe_name,      // All recipes commented on by the high-rep user
    count(DISTINCT u.user_name) AS reach,                // Number of other users in the same conversation network
    collect(DISTINCT u.user_name) AS users_reached       // List of those other users (network members)
;
