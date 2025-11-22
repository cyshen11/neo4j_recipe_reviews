/**
 * Header Comment: Identify Bridge Users Across Communities
 * 
 * Purpose:
 * Identifies "bridge users" - users who span multiple communities in the user co-comment network.
 * Bridge users are influential connectors who comment on recipes discussed across different 
 * community groups, making them valuable for cross-community insights and recommendations.
 * 
 * Algorithm Flow:
 * 1. Runs Louvain community detection on the 'userCoComment' projected graph
 * 2. Samples up to 5 members from each community
 * 3. Finds recipes commented on by sampled members
 * 4. Identifies users appearing in 2+ communities (bridge users)
 * 
 * Returns:
 * A deduplicated list of bridge users (user_name) who connect multiple communities.
 * - Column: user_name (string) - Username of bridge users
 * 
 * Use Case:
 * Bridge users are key influencers for community analysis and recommendation systems.
 */

// Step 1: Run Louvain community detection and stream results with node IDs and community assignments
CALL gds.louvain.stream('userCoComment')
YIELD nodeId, communityId
// Convert nodeId (internal graph ID) back to actual database node with user properties

WITH gds.util.asNode(nodeId) AS user, communityId
// Sort by community and user name to prepare for sampling
ORDER BY communityId, user.user_name

// Group users by their community membership
WITH communityId, collect(user) AS users
// Sample up to 5 users from each community (to avoid bias from large communities)
UNWIND users[0..5] AS user

// Find recipes that sampled users have commented on
OPTIONAL MATCH (user)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)

// Count how many distinct communities have interacted with each recipe
// Bridge users will appear on recipes linked to multiple communities
WITH r, COUNT(DISTINCT communityId) AS tribe_count, COLLECT(user) AS users
// Filter to recipes that span 2 or more communities (indicators of bridge content)
WHERE tribe_count >= 2

UNWIND users AS user

RETURN DISTINCT user.user_name AS user_name
ORDER BY user.user_name
;