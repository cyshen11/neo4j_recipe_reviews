
// /**
//  * PURPOSE: User Commenting Journey Pattern Analysis
//  * 
//  * This query identifies common commenting sequences (patterns) that users follow. It finds
//  * the first 3 recipes each user comments on in chronological order, then aggregates to find
//  * which multi-recipe commenting paths are most frequently shared across users. This reveals
//  * typical user onboarding or engagement sequences.
//  * 
//  * RETURNS:
//  *   - commenting_path: An ordered list of the first 3 recipes a user comments on (by timestamp)
//  *   - user_count: Number of users who followed this exact commenting sequence
//  */

// STAGE 1: For each user, fetch all their comments and their associated recipes
MATCH (r1:RECIPE) <- [:BELONGS_TO] - (c1:COMMENT) - [:POSTED] - (u:USER)

// Find all other comments from the same user on different recipes
// This creates a cartesian product of each user's first comment with all their other comments
MATCH (u)-[:POSTED]-(c2:COMMENT)-[:BELONGS_TO]->(r2:RECIPE)
WHERE c2 <> c1              // Exclude the first comment (avoid duplicates)
AND r2 <> r1                // Exclude the first recipe

// STAGE 2: Build a combined list of all comments with recipe and timestamp information
// Project user identity and create structured objects containing recipe names and timestamps
WITH u.user_name AS user,
    r1.recipe_name AS recipe1,
    c1.created_at AS created1,
    COLLECT({recipe: r2.recipe_name, created: c2.created_at}) AS other_comments

// Concatenate the first comment object with all subsequent comments into a single list
// This ensures we have a complete record of all user comments for sorting
WITH user,
    [{recipe: recipe1, created: created1}] + other_comments AS comments

// STAGE 3: Unwind and sort comments chronologically per user
// This flattens the comment list back into individual rows for proper temporal ordering
UNWIND comments AS c
WITH user, c.recipe AS recipe, c.created AS created
// Sort by user first (to maintain per-user grouping), then by creation time (chronological order)
ORDER BY user, created

// STAGE 4: Extract the first 3 recipes each user commented on (the commenting path/journey)
// Collect recipes per user and slice to get only the first 3 [0..3] to identify the commenting journey
WITH user,
    COLLECT(DISTINCT recipe)[0..3] AS commenting_path
// Filter out users who haven't commented on at least 3 distinct recipes (edge cases)
WHERE size(commenting_path) >= 3

// STAGE 5: Aggregate users by their commenting path to find common patterns
WITH commenting_path,
    COUNT(user) AS user_count       // Count how many users followed this exact sequence
// WHERE user_count > 1             // Optional: filter for patterns followed by multiple users

RETURN
    commenting_path,
    user_count
ORDER BY user_count DESC            // Show most common patterns first
;