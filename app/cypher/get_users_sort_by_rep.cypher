//
// Purpose: This query retrieves a list of all users in the database, sorted by their reputation score in descending order.
// It's a straightforward way to generate a user leaderboard or identify the most reputable users in the system for analysis.
//
// Returns:
// - user_name: The username of the user.
// - user_reputation: The reputation score of the user.
//

// Find all nodes with the label 'USER'.
MATCH (u:USER)
// Return the username and reputation for each user.
RETURN u.user_name AS user_name, u.user_reputation AS user_reputation
// Order the results by reputation in descending order (highest first) to create a ranked list.
ORDER BY u.user_reputation DESC