
/**
 * PURPOSE: Retrieves all comments posted by a specific user across all recipes
 * 
 * This query traverses the relationship graph to find comments authored by a given user,
 * then returns those comments with their engagement metrics and associated recipe information.
 * Results are ranked by popularity (thumbs_up count) in descending order.
 * 
 * RETURNS:
 *   - comment: The text content of the comment
 *   - thumbs_up: Count of positive votes/engagement for the comment
 *   - created_at: Timestamp when the comment was posted
 *   - recipe: The name of the recipe the comment belongs to
 */

// Find the pattern: RECIPE node -> connected via BELONGS_TO <- COMMENT node -> connected via POSTED <- USER node
// This pattern traverses relationships in reverse (using <-) to navigate from user through their comments to recipes
MATCH (r:RECIPE) <- [:BELONGS_TO] - (c:COMMENT) - [:POSTED] - (u:USER)

// Filter for only the specified user by matching their username parameter
WHERE u.user_name = '{user}'

// Project the relevant fields from the comment and recipe nodes, aliased for clarity
RETURN c.text AS comment, c.thumbs_up AS thumbs_up, c.created_at AS created_at, r.recipe_name AS recipe

// Sort results by engagement (descending), showing most popular/impactful comments first
ORDER BY c.thumbs_up DESC