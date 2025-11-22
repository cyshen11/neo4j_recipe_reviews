//
// Purpose: This query implements a collaborative filtering approach to find similar recipes.
// It identifies recipes that are "similar" to a given target recipe based on the number of users
// who have commented on both. This is a form of "users who liked this also liked..." recommendation.
//
// Returns:
// - recipe_name: The name of a similar recipe.
// - shared_commenter_count: The number of users who commented on both the target recipe and this similar recipe. This serves as the similarity score.
// - shared_commenters: A list of usernames for the users who commented on both recipes.
//

// Step 1: Find pairs of recipes (r1, r2) that have been commented on by the same user (u).
// This pattern represents the core of the collaborative filtering logic.
MATCH
    (r1:RECIPE) <- [:BELONGS_TO] - (:COMMENT) - [:POSTED] - (u:USER) - [:POSTED] - (:COMMENT) - [:BELONGS_TO] -> (r2:RECIPE)
WHERE
    // Ensure we are not comparing a recipe to itself.
    r1.recipe_name <> r2.recipe_name
    // Anchor the search to a specific target recipe provided as a parameter.
    AND r2.recipe_name = '{recipe}'

// Step 2: Aggregate the results to calculate the similarity score.
RETURN
    r1.recipe_name AS recipe_name,
    // Count the number of unique users who commented on both recipes. This is our similarity metric.
    COUNT(DISTINCT u) AS shared_commenter_count,
    // Collect the names of the shared commenters for additional insight.
    COLLECT(DISTINCT u.user_name) AS shared_commenters
// Step 3: Order the results to find the top N most similar recipes.
ORDER BY shared_commenter_count DESC
LIMIT 5
;