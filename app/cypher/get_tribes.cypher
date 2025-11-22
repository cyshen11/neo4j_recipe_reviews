//
// Purpose: This query identifies "tribes" or communities of users based on their commenting behavior.
// It uses the Louvain community detection algorithm on a graph of users connected by co-commenting on recipes.
// After identifying the communities, it samples a few users from each community and lists some of the recipes
// they have commented on to provide a qualitative sense of what defines each tribe.
//
// Returns:
// - communityId: The ID for the detected community (tribe).
// - user_name: The name of a sample user from that community.
// - recipe: The name of a recipe that the sample user has commented on.
// - user_count: The count of the user in that row (will always be 1).
//

// Step 1: Run the Louvain community detection algorithm on a pre-existing in-memory graph named 'userCoComment'.
// The Louvain algorithm is a popular method for finding community structures in large networks.
// It streams back each user's node ID and the community ID they've been assigned to.
CALL gds.louvain.stream('userCoComment')
YIELD nodeId, communityId

// Step 2: Convert the internal node IDs back to actual User nodes and order them by community.
WITH gds.util.asNode(nodeId) AS user, communityId
ORDER BY communityId, user.user_name

// Step 3: For each community, collect all its users into a list.
WITH communityId, collect(user) AS users
// Then, take a sample of up to the first 5 users from each community to analyze. This keeps the result set manageable.
UNWIND users[0..5] AS user

// Step 4: For each sampled user, find a recipe they have commented on.
// OPTIONAL MATCH is used in case a user in the graph hasn't posted any comments.
OPTIONAL MATCH (user)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)
// Step 5: Return the community, the sample user, and one of the recipes they commented on.
// This provides a snapshot of the types of recipes that are of interest to each community.
RETURN communityId, user.user_name AS user_name, r.recipe_name AS recipe, count(user) AS user_count
ORDER BY communityId, user_name, recipe
;