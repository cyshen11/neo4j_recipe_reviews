//
// Purpose: This query analyzes the "influencer effect" of high-reputation users on recipe reviews.
// It identifies the first 5-star comment from a top-100 reputation user for a specific recipe.
// It then calculates the total number of replies and thumbs-up on all subsequent comments for that same recipe,
// to measure the engagement lift following a positive review from an influential user.
//
// Returns:
// - user: The username of the high-reputation user.
// - user_reputation: The reputation score of that user.
// - comment: The text of their first 5-star comment.
// - created_at: The timestamp of that 5-star comment.
// - total_reply_count: The sum of replies for all comments posted *after* the influential comment.
// - total_thumbs_up: The sum of thumbs-up for all comments posted *after* the influential comment.
//

// Step 1: Identify the top 100 users by reputation score. These are considered our "influencers".
MATCH (top_users:USER)
ORDER BY top_users.user_reputation DESC
LIMIT 100

// Step 2: Find the earliest 5-star comment (`c1`) on a specific recipe posted by one of our top users.
// This comment acts as a temporal anchor or "pivot point" for our analysis.
MATCH (r:RECIPE) <- [:BELONGS_TO] - (c1:COMMENT) - [:POSTED] - (top_users)
WHERE c1.stars = 5
AND r.recipe_name = '{recipe}'
ORDER BY c1.created_at
LIMIT 1

// Step 3: Gather all comments (`c2`) on the same recipe that were posted *after* the influential 5-star comment.
MATCH (r) <- [:BELONGS_TO] - (c2:COMMENT) 
WHERE c2.created_at > c1.created_at

// Step 4: Return details of the influential user and their comment, along with aggregated engagement metrics from all subsequent comments.
RETURN 
    top_users.user_name AS user,
    top_users.user_reputation AS user_reputation,
    c1.text AS comment,
    c1.created_at AS created_at,
    // Sum the engagement metrics from all comments that came after the influencer's comment.
    SUM(c2.reply_count) AS total_reply_count, 
    SUM(c2.thumbs_up) AS total_thumbs_up
;