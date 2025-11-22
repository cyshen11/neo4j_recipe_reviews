// run Louvain and stream results
CALL gds.louvain.stream('userCoComment')
YIELD nodeId, communityId

WITH gds.util.asNode(nodeId) AS user, communityId
ORDER BY communityId, user.user_name

WITH communityId, collect(user) AS users
UNWIND users[0..5] AS user

OPTIONAL MATCH (user)-[:POSTED]-(:COMMENT)-[:BELONGS_TO]->(r:RECIPE)

WITH r, COUNT(DISTINCT communityId) AS tribe_count, COLLECT(user) AS users
WHERE tribe_count >= 2

UNWIND users AS user

RETURN DISTINCT user.user_name AS user_name
ORDER BY user.user_name
// LIMIT 100
;